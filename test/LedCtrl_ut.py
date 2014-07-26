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

        



if __name__ == "__main__":
    unittest.main()

# EOF