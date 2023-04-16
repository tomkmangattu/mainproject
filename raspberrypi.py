import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from smbus import SMBus
import time

addr = 0x10 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
        bus.write_byte(addr, 0x1)
        bus.write_byte(addr, 0x2)
        bus.write_byte(addr, 0x3)
        bus.write_byte(addr, 0x4)
        time.sleep(1)
