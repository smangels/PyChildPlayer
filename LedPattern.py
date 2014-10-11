import sys
from Led import Led

class LedPattern(object):

    # states (0=off,1=on,2=blink,3=pattern)
    
    LED_OFF = [ 0, 0, 0, 0]
    LED_ON = [ 1, 0, 0, 0]
    LED_BLINK = [ 5, 10, 0, 0 ]

    def __init__(self, pin):
        self._sequence = self.LED_OFF
        self._led = Led(pin)
        self._offTime = 0
        self._nrRep = 0
        self._pause = 0
        self._state = 0
        self._onTime = 0
        self._mode = "off"
            
    def getPin(self):
        return self._led.getPin()
        
    def tick(self):
        if self._mode == "blink" or self._mode == "pattern":
            if self._state == 1:
                if self._onTime > 0:
                    self._onTime -= 1
                else:
                    self._onTime = self._sequence[ 0 ] - 1
                    self._led.off()
                    self._state = 2
            elif self._state == 2:
                if self._offTime > 0:
                    self._offTime -= 1
                else:
                    self._offTime = self._sequence[ 1 ] - 1
                    self._state = 1
                    self._led.on()
            else:
                self._state = 1
                self._led.on()
        elif self._mode == "on":
            if self._state == 0:
                self._led.on()
                self._state = 1
            else:
                pass
        elif self._mode == "off":
            if self._state == 0:
                self._led.off()
                self._state = 1
            else:
                pass
        else:
            print "unknown mode"


    def setSequence(self, seq):
        self._sequence = seq
        self._initCntr()
        self._mode = self._parseSequence(seq)
        print "setSequence, new mode: %s" % self._mode

    def getMode(self):
	    return self._mode

    def getSequence(self):
        return self._sequence
        
    def _parseSequence(self, seq):
        if seq[ 0 ] > 0 and seq [ 1 ] > 0:
            return "blink"
        elif seq[ 0 ] > 0 and seq[ 1 ] == 0:
            return "on"
        elif seq[ 0 ] == 0:
            return "off"
        else:
            return "invalid"

    def _initCntr(self):
            self._onTime  = self._sequence[ 0 ] - 1
            self._offTime = self._sequence[ 1 ] - 1
            self._nrRep   = self._sequence[ 2 ] - 1
            self._pause   = self._sequence[ 3 ] - 1
            self._state = 0
