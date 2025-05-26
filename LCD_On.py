import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

import adafruit_character_lcd.character_lcd_i2c as character_lcd

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# LCD configuration
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Clear and display a message
lcd.clear()
lcd.message = "Hello, Raspberry\nPi 3 B+ LCD!"

time.sleep(5)
lcd.clear()