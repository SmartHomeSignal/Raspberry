import RPi.GPIO as GPIO
import time
import asyncio
from network import Network

RUNNING = True
ISDETECTED = False
network = Network()
# GPIO SETUP
sound = 23
led = 27

Buzzer_PIN = 24

green = 27
red = 22
blue = 22

swPin = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(sound, GPIO.IN)

GPIO.setup(Buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)

GPIO.setup(red, GPIO.OUT, initial= GPIO.LOW)
#GPIO.setup(green, GPIO.OUT, initial= GPIO.LOW)
#GPIO.setup(blue, GPIO.OUT, initial= GPIO.LOW)

GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def eventSWButton(e):
    print("SW from joystick pressed")
    GPIO.output(Buzzer_PIN, GPIO.LOW)
    GPIO.output(red, GPIO.LOW)
    print(e)

def test(channel):
    global ISDETECTED
    if channel == 23:
        print("sound")
        ISDETECTED = True
        network.enable_signal()
    else:
        print("button")
        ISDETECTED = False
        network.disable_signal()

def callback(is_signal_on):
    global ISDETECTED
    if is_signal_on:
        print("Enable signal")
        ISDETECTED = True
    else:
        print("Disable signal")
        ISDETECTED = False
try:
    GPIO.add_event_detect(sound, GPIO.RISING, bouncetime = 200, callback = test)
    GPIO.add_event_detect(swPin, GPIO.FALLING, bouncetime = 200, callback = test)
    network.connect(callback)
    while RUNNING:
        if ISDETECTED:
            print("SOUND DETECTED")
            GPIO.output(Buzzer_PIN, GPIO.HIGH)  # Buzzer will be switched on 
            GPIO.output(red, GPIO.HIGH)
            time.sleep(0.5)  
            GPIO.output(red,GPIO.LOW) #LED will be switched ON
            time.sleep(0.5)
        else:
            GPIO.output(Buzzer_PIN, GPIO.LOW)
            GPIO.output(red, GPIO.LOW)
   
except KeyboardInterrupt:
    RUNNING = False
    GPIO.cleanup()
    network.disconnect()