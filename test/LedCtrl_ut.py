# test LedCtrl class

import unittest
import sys

sys.path.append('../')

from LedCtrl import Led


class TestSequence(unittest.TestCase):

        def setUp(self):
                pass

        def test_createLed(self):

                cmds = [ "blink", "on", "off" ]
                
                ledYellow = Led("ledYellow", 23)
                ledGreen = Led("ledGreen", 21)
                ledRed = Led("ledRed", 22)

                print ledYellow
                print ledGreen
                print ledRed



if __name__ == "__main__":
    unittest.main()

# EOF