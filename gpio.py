import RPi.GPIO as GPIO
import signal
import sys
#import picamera
import time
import zbar
import io
#from PIL import Image
from mpdclient import mpdclient

def led_all_off():
	for led in led_all:
		GPIO.output(led, GPIO.LOW)

def get_qr_content(string):
	qr_content = string.split(',')
	print qr_content
	dict = {}
	for item in qr_content:
		row = item.split('=')
		if len(row) == 2:
			dict[ row[ 0 ].strip() ] = row[ 1 ].strip("\"")
		else:
			print "invalid row"
	print dict
	return dict
		
def cam_capture():
    	# Camera warm-up time
    	# camera.capture('qr.jpg', resize=(320, 240))
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg')
	stream.seek(0)
	pil = Image.open(stream)
	scanner =zbar.ImageScanner()
	scanner.parse_config('enable')
	pil = pil.convert('L')
	width, height = pil.size
	raw = pil.tostring()
	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)
	for symbol in image:
		# print 'decode', symbol.type, 'symbol', '"%s"' % symbol.data
		print type(symbol.type)
		if symbol.type == 64:
			print ("QR detected")
			dict = get_qr_content(symbol.data)
			client.add(dict['folder'])
			
		else:
			print ("no QR code, type: %s" % symbol.type )
	del image
	stream.close()

def printFunction(channel):
	global led_flag
	print("PIN is %d" % led_flag)

	if (GPIO.input(sens) == 1):
		print "is high => return"
		return

	if (led_flag == 1):
		GPIO.output(led_red, GPIO.LOW)
		led_flag = 0
	else:
		GPIO.output(led_red, GPIO.HIGH)
		led_flag = 1

	
def signal_handler(signal, frame):
	print ("Ctrl-C detected")
	led_all_off()
	GPIO.cleanup()
	sys.exit()
	
# supposed to use the board numbering
GPIO.setmode(GPIO.BCM)

signal.signal(signal.SIGINT, signal_handler)

# configure GPIOs
led_flag = 1
sens = 23
led_yellow = 27
led_green = 22
led_red = 17
led_all = [led_yellow, led_green, led_red]
sens_bounce_ms = 300

GPIO.setup(sens, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_yellow, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
print "initiated: GPIO"

GPIO.output(led_red, GPIO.HIGH)
GPIO.output(led_yellow, GPIO.HIGH)
GPIO.output(led_green, GPIO.HIGH)

GPIO.add_event_detect(sens, GPIO.FALLING, callback=printFunction, bouncetime=sens_bounce_ms)
	

signal.pause()

exit ()
