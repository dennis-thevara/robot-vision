from nanpy import ArduinoApi
from nanpy import SerialManager
from time import sleep

link = SerialManager(device='/dev/ttyACM0')
A = ArduinoApi(connection=link)

led = 13

# SETUP:
A.pinMode(led, A.OUTPUT)

# LOOP:
while True:
    A.digitalWrite(led, A.HIGH) # turn the LED on (HIGH is the voltage level)
    print "blink on"
    sleep(1) # use Python sleep instead of arduino delay
    A.digitalWrite(led, A.LOW) # turn the LED off by making the voltage LOW
    print "blink off"
    sleep(1)
