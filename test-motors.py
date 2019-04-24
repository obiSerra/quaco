# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
#GPIO.setmode(GPIO.BCM)
mode=GPIO.getmode()
print(" mode = {}".format(str(mode)))
#GPIO.cleanup()

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24

aForward=15
aBackward=18

bForward=22
bBackward=16
sleeptime=1

GPIO.setmode(GPIO.BOARD)

GPIO.setup(aForward, GPIO.OUT)
GPIO.setup(aBackward, GPIO.OUT)
GPIO.setup(bForward, GPIO.OUT)
GPIO.setup(bBackward, GPIO.OUT)

def forward(a, b):
    if a:        
        GPIO.output(aForward, GPIO.HIGH)
    if b:
        GPIO.output(bForward, GPIO.HIGH)

def backward(a, b):
    if a:
        GPIO.output(aBackward, GPIO.HIGH)
    if b:
        GPIO.output(bBackward, GPIO.HIGH)

def stop(a, b):
    if a:
        GPIO.output(aForward, GPIO.LOW)
        GPIO.output(bForward, GPIO.LOW)
    if b:
        GPIO.output(aBackward, GPIO.LOW)
        GPIO.output(bBackward, GPIO.LOW)

def stopAll():
    GPIO.output(aForward, GPIO.LOW)
    GPIO.output(bForward, GPIO.LOW)
    GPIO.output(aBackward, GPIO.LOW)
    GPIO.output(bBackward, GPIO.LOW)
        
print("Forward A")
forward(True, True)
time.sleep(2)
stopAll()
print("Forward B")
backward(True, True)
time.sleep(2)
stopAll()
GPIO.cleanup()
