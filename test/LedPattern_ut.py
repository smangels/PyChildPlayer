
import unittest
import sys
import RPi.GPIO as GPIO


from time import sleep


sys.path.append("../")

from LedPattern import LedPattern


class TestSequence(unittest.TestCase):

    def setUp(self):
        GPIO.setmode(GPIO.BCM)
        self.pattern = None
        
    def tearDown(self):
        del self.pattern
        GPIO.cleanup()
        
    def test_createPattern(self):
        self.pattern = LedPattern(17)
        self.pattern.setSequence([5, 5, 2, 10])
        for step in range(100):
            sleep(0.05)
            self.pattern.tick()
            if step == 1:
                self.assertEqual(GPIO.input(17), 1)
        self.pattern.getSequence()
        self.pattern.getMode()
        
    def test_JustOn(self):
        self.pattern = LedPattern(17)
        self.pattern.setSequence([1, 0, 0, 0])
        for step in range(100):
            sleep(0.05)
            self.pattern.tick()
            self.assertEqual(GPIO.input(17), 1)

    def test_JustOff(self):
        self.pattern = LedPattern(17)
        self.pattern.setSequence([0,0,0,0])
        for step in range(100):
            sleep(0.05)
            self.pattern.tick()
            self.assertEqual(GPIO.input(17), 0)

if __name__ == "__main__":
    unittest.main()
    
