
import threading
import time
import Queue
import signal
from LedPattern import LedPattern



def signal_handler(signal, frame):
        print ("Ctrl-C detected")
        sys.exit()

def ledThread(listLed, cmdQueue, period=1):
        myThreadId = threading.current_thread()
        exit_flag = False
        print " >> init threading"
        
        while not exit_flag:
            try:
                cmd = cmdQueue.get(block=True, timeout=0.05)
            except Queue.Empty:
			    continue
            else:
                if cmd[0] == "exit":
                    exit_flag = True
                elif cmd[0] == "cmd":
                    if len(cmd) < 3:
                        print "!! invalid command"
                        continue
                    else:
                        print "received a command for LED %d" % cmd[1]
                        for led in listLed:
                            if cmd[1] == led.getPin():
                                led.setSequence(cmd[2])
                                print "switched LED %d to ON, pattern: %s" % (cmd[1], cmd[2])
                                break
                else:
                    print "unknown command in queue"

        print "finished THREAD"

class LedCtrl(object):

	# defines for frequently used LED pattern

    def __init__(self):
        self._running = False
        self._queue = Queue.Queue(10)
        self._ledList = []
        return None
        
    def __del__(self):
        if self._running == True:
            self._queue.put("exit")
            self._thread.join()
            return None

    def addLed(self, pin):
        for led in self._ledList:
            if (pin == led.getPin):
                print "failed to add, does already exist"
                return False
        self._ledList.append(LedPattern(pin))
        return True

	def sendCmd(self, pin, sequence):
		if self._running == True:
			self._queue.put(["cmd", pin, sequence])
			print "send cmd for pin %d" % pin
		else:
			print "no thread - no queue"

		return False
        
	def startThread(self):
		if not self._running:
		 	self._thread = threading.Thread(target=ledThread, args=(self._ledList, self._queue, 1) )
                	self._thread.daemon = True
			self._thread.start()
			self._running = True
			print "thread started"
			return None
		else:
			print "tread is already running"
			return False

	def stopThread(self):
		if self._running == True:
			self._queue.put(["exit"])
			self._thread.join()
			self._running = False
			print "EXIT sent to thread"
		else:
			print "no thread running"

        def __str__(self):
                s = "currently not implemented"
		for led in self._ledList:
			print led
                return s


# EOF
