import serial

# Configure serial port for GY-NEO6MV2 (default baudrate is 9600)
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

def read_gps():
    while True:
        line = ser.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            print(line)

if __name__ == "__main__":
    try:
        print("Reading GPS data...")
        read_gps()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()