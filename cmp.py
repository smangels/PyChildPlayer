
from LedCtrl import LedCtrl
import signal
import sys
from time import sleep
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
	sys.exit()

GPIO.setmode(GPIO.BCM)

led_green = 17
led_red = 27
led_yellow = 23

ledCtrl = LedCtrl()
ledCtrl.addLed(led_green)
ledCtrl.addLed(led_red)
ledCtrl.addLed(led_yellow)


ledCtrl.startThread()


ledCtrl.sendCmd(led_green, ledCtrl.LED_ON)


sleep(2)


