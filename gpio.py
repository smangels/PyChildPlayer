import RPi.GPIO as GPIO
import signal
import sys
import picamera
import time
import zbar
import io
from PIL import Image
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
	print ("edge: %d" % channel)
	if (GPIO.input(sens) == 1):
		GPIO.output(led_red, GPIO.HIGH)
		print ("QR tag detected")
		cam_capture()
		print ("image take")
	else:
		GPIO.output(led_red, GPIO.LOW)
		client.pause()
		print ("QR tag removed")
	
def signal_handler(signal, frame):
	print ("Ctrl-C detected")
	led_all_off()
	GPIO.cleanup()
	sys.exit()
	
# supposed to use the board numbering
GPIO.setmode(GPIO.BCM)

signal.signal(signal.SIGINT, signal_handler)

# configure GPIOs
sens = 23
led_yellow = 17
led_green = 27
led_red = 22
led_all = [led_yellow, led_green, led_red]
sens_bounce_ms = 150

GPIO.setup(sens, GPIO.IN)
GPIO.setup(led_yellow, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
print "initiated: GPIO"

GPIO.output(led_red, GPIO.LOW)

exit()

camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(2)
print "initiated: camera module"

client = mpdclient()
# client.add("Alexi Murdoch/Towards The Sun")
print "initiated: MPD"


if (GPIO.input(sens) == 1):
	print ("enabled FALLING")
	GPIO.add_event_detect(sens, GPIO.FALLING, callback=printFunction, bouncetime=sens_bounce_ms)
else:
	print ("enabled RISING")
	GPIO.add_event_detect(sens, GPIO.RISING, callback=printFunction, bouncetime=sens_bounce_ms)
	

signal.pause()

