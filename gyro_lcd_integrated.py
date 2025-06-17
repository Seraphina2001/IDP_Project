import smbus
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# MPU6050 Registers and their Address
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43

# Initialize I2C bus for MPU6050
bus = smbus.SMBus(1)  # For Raspberry Pi 3 B+

# Initialize I2C for LCD
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    lcd_columns = 16
    lcd_rows = 2
    
    # Try to detect LCD at different I2C addresses
    lcd_addresses = [0x27, 0x3F]  # Common LCD I2C addresses
    lcd = None
    
    for addr in lcd_addresses:
        try:
            lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, addr)
            print(f"LCD found at address: 0x{addr:02X}")
            break
        except Exception as e:
            print(f"No LCD at address 0x{addr:02X}: {str(e)}")
            continue
    
    if lcd is None:
        raise Exception("No LCD display found. Please check connections.")
        
except Exception as e:
    print(f"Error initializing LCD: {str(e)}")
    print("Please check:")
    print("1. LCD is properly connected to SDA and SCL pins")
    print("2. I2C is enabled (sudo raspi-config)")
    print("3. LCD has power (VCC to 5V)")
    print("4. Ground connection is secure")
    exit(1)

def mpu6050_init():
    try:
        bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)
        print("MPU6050 initialized successfully")
    except Exception as e:
        print(f"Error initializing MPU6050: {str(e)}")
        print("Please check MPU6050 connections")
        exit(1)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

def update_lcd(message):
    try:
        lcd.clear()
        lcd.message = message
    except Exception as e:
        print(f"Error updating LCD: {str(e)}")

def main():
    print("Starting Gyro-Accelerometer and LCD system...")
    mpu6050_init()
    update_lcd("System Ready\nMonitoring...")
    time.sleep(2)
    
    try:
        while True:
            # Read Accelerometer raw values
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_XOUT_H+2)
            acc_z = read_raw_data(ACCEL_XOUT_H+4)

            # Read Gyroscope raw values
            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_XOUT_H+2)
            gyro_z = read_raw_data(GYRO_XOUT_H+4)

            # Convert to actual values
            Ax = acc_x/16384.0
            Ay = acc_y/16384.0
            Az = acc_z/16384.0

            Gx = gyro_x/131.0
            Gy = gyro_y/131.0
            Gz = gyro_z/131.0

            # Create display message
            display_message = f"Accel: {Ax:.2f}g\nGyro: {Gx:.1f}°/s"
            update_lcd(display_message)
            
            # Print values to console as well
            print(f"Ax={Ax:.2f}g\tAy={Ay:.2f}g\tAz={Az:.2f}g\tGx={Gx:.2f}°/s\tGy={Gy:.2f}°/s\tGz={Gz:.2f}°/s")
            
            time.sleep(0.5)  # Update every 0.5 seconds

    except KeyboardInterrupt:
        update_lcd("System Shutdown\nGoodbye!")
        time.sleep(2)
        lcd.clear()
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
        update_lcd("System Error\nCheck Console")
        time.sleep(5)

if __name__ == "__main__":
    main() 