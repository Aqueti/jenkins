
import RPi.GPIO as GPIO
import time

pin = 11

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.LOW)
time.sleep(1)
GPIO.output(pin, GPIO.HIGH)
        