import smbus
import time

# MPU6050 Registers and their Address
MPU6050_ADDR = 0x68
PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43

bus = smbus.SMBus(1)  # For Raspberry Pi 3 B+

def mpu6050_init():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr+1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

mpu6050_init()

try:
    while True:
        # Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_XOUT_H+2)
        acc_z = read_raw_data(ACCEL_XOUT_H+4)

        # Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_XOUT_H+2)
        gyro_z = read_raw_data(GYRO_XOUT_H+4)

        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0

        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        print("Ax=%.2f g\tAy=%.2f g\tAz=%.2f g\tGx=%.2f °/s\tGy=%.2f °/s\tGz=%.2f °/s" % (Ax, Ay, Az, Gx, Gy, Gz))
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")
