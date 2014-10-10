import RPi.GPIO as GPIO


class Led(object):
	def __init__(self, pin, name="led"):
		self._pin = pin
		self._state = False
		self._name = name
		GPIO.setup(self._pin, GPIO.OUT)
		GPIO.output(self._pin, GPIO.LOW)
		print "create LED for pin %d" % pin

	def off(self):
		GPIO.output(self._pin, GPIO.LOW)

	def on(self):
		GPIO.output(self._pin, GPIO.HIGH)

	def getPin(self):
		return self._pin

	def __del__(self):
		GPIO.output(self._pin, GPIO.LOW)
		return None

	def __str__(self):
		s = "LED: %s(%d), current state" % (self._name, self._pin)
		return s
