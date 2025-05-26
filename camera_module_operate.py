import time
from picamera import PiCamera

def capture_image(filename='image.jpg'):
    camera = PiCamera()
    try:
        camera.start_preview()
        time.sleep(2)  # Camera warm-up time
        camera.capture(filename)
        print(f"Image saved as {filename}")
    finally:
        camera.stop_preview()
        camera.close()

if __name__ == "__main__":
    capture_image()