import RPi.GPIO as GPIO
import unittest
import sys
from time import sleep

sys.path.append('../')

from Led import Led


class TestSequence(unittest.TestCase):

        def setUp(self):
		GPIO.setmode(GPIO.BCM)
                self.led = None
		print "SETUP finished"

	def tearDown(self):
		pin = self.led._pin
		del self.led
		self.assertEqual(GPIO.input(pin), 0)
		GPIO.cleanup()
		print "DESTROY finished"

        def test_createLedYellow(self):
                self.led       = Led(27, "yellow LED")
		print self.led
		self.assertEqual(GPIO.input(27), 0)
		self.led.on()
		sleep(1)
		self.assertEqual(GPIO.input(27), 1)
		return None

	def test_createLedRed(self):
		self.led = Led(17, "red LED")
		print self.led
		self.assertEqual(GPIO.input(17), 0)
		print GPIO.input(17)
		self.led.on()
		sleep(1)
		self.assertEqual(GPIO.input(17), 1)
		return None

if __name__ == "__main__":
    unittest.main()

# EOF



