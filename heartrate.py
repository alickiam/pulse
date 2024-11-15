import pigpio

# I2C address of the multiplexer
TCAADDR = 0x70
# I2C address of the heart rate sensor (both have same address)
MAXADDR = 0x57

# pigpio command codes for i2c_zip()
Z_END = 0
Z_READ = 6
Z_WRITE = 7

# Heart rate sensor register addresses
MAX_INT_1 = 0x00
MAX_INT_2 = 0x01
MAX_INT_EN_1 = 0x02
MAX_INT_EN_2 = 0x03
MAX_FIFO_WR_PTR = 0x04
MAX_OVF_COUNTER = 0x05
MAX_RD_PTR = 0x06
MAX_FIFO_DATA = 0x07
MAX_FIFO_CONF = 0x08
MAX_MODE_CONF = 0x09
MAX_SPO2_CONF = 0x0a
MAX_LED1_PA = 0x0c
MAX_LED2_PA = 0x0d
MAX_TINT = 0x1f
MAX_TFRAC = 0x20
MAX_TEMP_EN = 0x21
MAX_PART_ID = 0xff

# Heart rate sensor constants
MAX_DIE_TEMP_RDY_F = 1 << 1

class HeartRateManager:
    def __init__(self):
        # Initialize GPIO
        self.pi = pigpio.pi()

        # Open I2C multiplexer on bus 1
        self.tca_handle = self.pi.i2c_open(1, TCAADDR)
        # Open heart rate sensor on bus 1
        self.max_handle = self.pi.i2c_open(1, MAXADDR)

        self.current_sensor_num = -1

        # Ensure connection to sensors exists
        for i in range(2):
            print(f"Setting up sensor {i}...", end="")
            self.select_sensor(i)
            assert self.pi.i2c_read_byte_data(self.max_handle, MAX_PART_ID) == 0x15
            # Enable temperature ready flag
            self.pi.i2c_write_byte_data(self.max_handle, MAX_INT_EN_2, MAX_DIE_TEMP_RDY_F)
            # Reset FIFO
            self.pi.i2c_zip(self.max_handle, [Z_WRITE, 4, MAX_FIFO_WR_PTR, 0, 0, 0, Z_END])
            print(" OK")

    def select_sensor(self, num):
        """Switch communication over I2C to the given sensor number, 0 or 1."""
        if num != 0 and num != 1:
            raise ValueError(f"Invalid sensor number {num}")
        if num == self.current_sensor_num:
            return
        self.pi.i2c_write_byte(self.tca_handle, 1 << num)
        self.current_sensor_num = num

    def read_temp(self, sensor_num):
        """Read the current temperature from the given sensor as a float, or -1 if failed."""
        self.select_sensor(sensor_num)

        # Start temperature reading
        self.pi.i2c_write_byte_data(self.max_handle, MAX_TEMP_EN, 1)
        # Wait until the temperature reading is ready
        while True:
            r = self.pi.i2c_read_byte_data(self.max_handle, MAX_INT_2)
            if r & MAX_DIE_TEMP_RDY_F != 0:
                break

        # Get temperature reading
        (count, data) = self.pi.i2c_zip(self.max_handle, [Z_WRITE, 1, MAX_TINT, Z_READ, 2, Z_END])
        if count != 2:
            print("Unknown read_temp() data:", (count, data))
            return -1
        return int(data[0]) + (int(data[1]) * 0.0625)

    def stop(self):
        """Close all GPIO resources."""
        self.pi.i2c_close(self.max_handle)
        self.pi.i2c_close(self.tca_handle)
        self.pi.stop()
