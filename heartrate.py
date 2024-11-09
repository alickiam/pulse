import pigpio

# I2C address of the multiplexer
TCAADDR = 0x70
# I2C address of the heart rate sensor (both have same address)
MAXADDR = 0x57

# Initialize GPIO
pi = pigpio.pi()

# Open I2C multiplexer on bus 1
tca_handle = pi.i2c_open(1, TCAADDR)

def select_sensor(num):
    """Switch communication over I2C to the given sensor number, 0 or 1."""
    if num != 0 and num != 1:
        raise ValueError(f"Invalid sensor number {num}")
    pi.i2c_write_byte(tca_handle, 1 << num)

# Clean up
pi.i2c_close(tca_handle)
pi.stop()
