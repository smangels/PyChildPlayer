# test LedCtrl class

import unittest
import sys

sys.path.append('../')

from LedCtrl import Led


class TestSequence(unittest.TestCase):

        def setUp(self):
                self.led = None
                self.led       = Led("ledYellow", 23)

        def test_createLed(self):
                cmds = [ "blink", "on", "off" ]
                self.assertTrue(isinstance(self.led, Led))
        
        def test_pinCorrect(self):
                self.assertTrue(self.led.getPin() == 23)

        def test_nameCorrect(self):
                self.assertTrue(self.led.getState() == "off")

        def test_getStateChange(self):
                # perform a state change and check the resulting 
                # state using the provided interface
                self.assertTrue(self.led.getState() == "off")
                self.led.blink(10, 20)
                self.assertTrue(self.led.getState() == "blink")


if __name__ == "__main__":
    unittest.main()

# EOF