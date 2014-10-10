
from LedCtrl import LedCtrl
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
	GPIO.cleanup()
	sys.exit()

GPIO.setmode(GPIO.BCM)

led_green = 27
led_red = 17
led_yellow = 23

ledCtrl = LedCtrl()

ledCtrl.addLed(led_green)
ledCtrl.addLed(led_red)
ledCtrl.addLed(led_yellow)


ledCtrl.startThread()

print "started thread"
sleep(5)
ledCtrl.sendCmd(led_green, LedCtrl.LED_ON)
sleep(1)
ledCtrl.sendCmd(led_red, LedCtrl.LED_ON)
sleep(5)
ledCtrl.stopThread()
sleep(3)
exit(0)

