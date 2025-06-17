# IDP_Project
Automatic Car Crash Detection System

## Hardware Requirements
- Raspberry Pi 3 B+ or newer
- MPU6050 Gyro-Accelerometer Module
- 16x2 LCD Display with I2C interface
- Jumper wires

## Hardware Connections

### MPU6050 Connections
- VCC → 3.3V
- GND → GND
- SCL → GPIO3 (SCL)
- SDA → GPIO2 (SDA)

### LCD Display Connections
- VCC → 5V
- GND → GND
- SCL → GPIO3 (SCL)
- SDA → GPIO2 (SDA)

## Software Setup
1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Enable I2C on Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options → I2C → Enable
   ```

3. Run the accident detection system:
   ```bash
   python accident_detection.py
   ```

## System Operation
- The system continuously monitors acceleration and rotation
- LCD displays current system status
- Accident is detected when:
  - Acceleration exceeds 2.0g
  - Rotation exceeds 200°/s
- Both conditions must be met simultaneously to trigger accident detection
