
import threading
import time
import Queue
import signal
from Led import Led



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
                        # queue is empty, timeout occurred
			continue
                else:
                        # queue contains a new command, decode and run
                        if cmd == "exit":
                                exit_flag = True
				print "exit the thread %d" % myThreadId

			elif cmd == "cmd":
				print "received a command for LED %d" % cmd[1]

			else:
				print "invalid command in queue"

	print "finished THREAD %d " % myThreadId

class LedCtrl(object):

	# defines for frequently used LED pattern
	LED_OFF = [ 0, 0, 0, 0 ]
	LED_ON  = [ 1, 0, 0, 0 ]
	LED_BLINK = [ 5, 10, 0, 0 ]
	LED_ERR_INVALID_QR_CODE = [ 5, 10, 3, 20 ]


        def __init__(self):
		self._running = False
                self._queue = Queue.Queue(2)
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

		self._ledList.append(Led(pin))
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
		 	self._thread = threading.Thread(target=ledThread, args=(self._ledList, self._queue, 1) ).start()
                	#self._thread.daemon = True
			#self._thread.start()
			self._running = True
			print "thread started"
			return None
		else:
			print "tread is already running"
			return False

	def stopThread():
		if self._running == True:
			self._queue.put("exit")
			print "EXIT sent to thread"
		else:
			print "no thread running"

        def __str__(self):
                s = "currently not implemented"
		for led in self._ledList:
			print led
                return s


# EOF
