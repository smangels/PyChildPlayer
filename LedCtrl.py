
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
                        if cmd == "exit":
                                exit_flag = True
                        else:
                                print " >> pin:%d => received: %s \n" % (pin, cmd)
                                if cmd[0] == "blink":
                                        print " >> pin %d mode blink" % pin
                                        if cmd[1] < period:
                                                exit_flag = True
                                        else:
                                                mode = cmd[0]
                                                cntr_on = (cmd[1] / period) - 1
                                                cntr_off = (cmd[2] / period) - 1
                                                print (" >> pin %d, %d/%d" % (pin, cntr_on, cntr_off))
                                elif cmd[0] == "off":
                                        print " >> pin %d, OFF" % pin
                                        mode = "off"
                                elif cmd[0] == "on":
                                        print " >> pin %d, ON" % pin
                                        mode = "on"
                                cmd = ""
                                cntr += 1

        print " >> exit thread: %d, cntr=%d" % (pin, cntr)


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
                print("LED.init: new LED object %s, state=%s" % (self._name, self._state) )
        
        def __del__(self):
                self.off()
                self._queue.put("exit")
                self._thread.join()
                print("Led: finished destructor for %s" % self._name)
        
        def blink(self, onTime, offTime):
                self._queue.put([ "blink", onTime, offTime])
        
        def off(self):
                self._queue.put( ["off"])


def main():

        signal.signal(signal.SIGINT, signal_handler)

        cmds = [ "blink", "on", "off" ]
        
        ledYellow = Led("ledYellow", 23)
        ledGreen = Led("ledGreen", 21)
        ledRed = Led("ledRed", 22)

        print ("all threads created")

        ledYellow.blink(1, 0.5)
        ledGreen.blink(2, 0.5)
        ledRed.blink(2, 0.5)

        time.sleep(20)


    
if __name__ == "__main__":
    main()

# EOF