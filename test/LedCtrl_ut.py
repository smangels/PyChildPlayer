# test LedCtrl class

import unittest
import sys 
import RPi.GPIO as GPIO
from time import sleep

sys.path.append('../')

from LedCtrl import LedCtrl
	

class TestSequence(unittest.TestCase):

        def setUp(self):
                self.ctrl = None
		GPIO.setmode(GPIO.BCM)

	def tearDown(self):
		del self.ctrl
		GPIO.cleanup()

        def test_createLed(self):
		self.ctrl = LedCtrl()
		self.ctrl.addLed(17)
		self.ctrl.addLed(27)
		self.ctrl.addLed(22)
                self.assertTrue(isinstance(self.ctrl, LedCtrl))

	def test_switchLedOn(self):
		self.ctrl = LedCtrl()
		self.ctrl.addLed(17)
		self.ctrl.addLed(27)
		self.ctrl.startThread()
		self.ctrl.sendCmd(17, self.ctrl.LED_ON)
		self.ctrl.stopThread()

if __name__ == "__main__":
    unittest.main()

# EOF
