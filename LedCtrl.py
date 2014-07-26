
import threading
import time
import Queue
import signal

def signal_handler(signal, frame):
        print ("Ctrl-C detected")
        sys.exit()

def ledThread(cmdQueue, pin, period=1):
        myThreadId = threading.current_thread()
        exit_flag = False
        cmd = cmdQueue.get()
        cntr = 0
        onTime = 0
        offTime = 0
        mode = ""
        state = "off"
        print " >> init thread for pin %d, period=%2.3f" % (pin, period)
        
        while not exit_flag:
                try:
                        cmd = cmdQueue.get(block=True, timeout=1)
                except Queue.Empty:
                        # queue is empty, blocking call returns with exception
                        if mode == "blink":
                                if state == "off":
                                        if cntr > 0:
                                                cntr -= 1
                                        else:
                                                print " >> pin %d invert" % pin
                                                state = "on"
                                                cntr = onTime
                                elif state == "on":
                                        if cntr > 0:
                                                cntr -= 1
                                        else:
                                                print " >> pin %d invert" % pin
                                                state = "off"
                                                cntr = offTime

                else:
                        # queue contains a new command, decode and run
                        if cmd == "exit":
                                exit_flag = True
                        else:
                                #print " >> pin:%d => received: %s \n" % (pin, cmd)
                                if cmd[0] == "blink":
                                        #print " >> pin %d mode blink" % pin
                                        if cmd[1] < period:
                                                exit_flag = True
                                        else:
                                                mode = cmd[0]
                                                cntr_on = (cmd[1] / period) - 1
                                                cntr_off = (cmd[2] / period) - 1
                                                #print (" >> pin %d, %d/%d" % (pin, cntr_on, cntr_off))
                                elif cmd[0] == "off":
                                        #print " >> pin %d, OFF" % pin
                                        mode = "off"
                                elif cmd[0] == "on":
                                        #print " >> pin %d, ON" % pin
                                        mode = "on"

                                cmd = ""
                                cntr += 1


class Led(object):

        def __init__(self, name, pin, state=False, period=0.25):
                self._name = name
                self._pin = pin
                self._state = state
                self._queue = Queue.Queue(2)
                self._thread = threading.Thread(target=ledThread, args=(self._queue, self._pin, period) )
                self._thread.daemon = True
                self.off()
                self._thread.start()
                # print("LED.init: new LED object %s, state=%s" % (self._name, self._state) )
                return None
        
        def __del__(self):
                self.off()
                self._queue.put("exit")
                self._thread.join()
                #print("Led: finished destructor for %s" % self._name)
                return None
        
        def blink(self, onTime, offTime):
                self.state = "blink"
                self._queue.put([ "blink", onTime, offTime])
                return self.state
        
        def off(self):
                self.state = "off"
                self._queue.put( ["off"] )
                return self.state

        def on(self):
                self.state = "on"
                self._queue.put( ["on"] )
                return self.state

        def getState(self):
                return self._state

        def getPin(self):
                return self._pin

        def __str__(self):
                s = "Led (%s), Pin=%d, State=%s" % (self._name, self._pin, self._state)
                return s


# EOF