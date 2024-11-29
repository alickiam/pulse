# SE 101 Project

Team 14:
- Martin Baldwin
- Alex Du
- Alicia Mao
- Faisal Sayed
- Shivani Tiwari
- Michelle Yao

## GPIO Setup

```
..1..2............3.
456..............7..
```
1. Ground
2. Mic BCLK
3. Mic DOUT
4. 3.3V
5. I2C data
6. I2C clock
7. Mic LRCL

## Software Setup

1. Turn on iphslamma hotspot

### Host
1. Install Python packages from requirements.txt
2. Ensure venv is activated
3. Ensure OpenAI API key environment variable is set
4. Ensure SSH identity is added

### Raspberry Pi
1. Start pigpio daemon with `sudo pigpiod -t 0`
   - `-t 0` is necessary to avoid interfering with I2S microphone input
2. Ensure `$HOME/record` directory exists
