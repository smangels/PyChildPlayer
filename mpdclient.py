from mpd import MPDClient


class mpdclient(object):
	def __init__(self, host="localhost", port=6600):
		self.client = MPDClient()
		self.timeout = 10
		self.idletimeout = None
		self.client.connect(host, port)
		self.client.clear()
		print "MPD version %s" % self.client.mpd_version
		print "mpdclient -> constructor done"
	
	def __del__(self):
		if self.client != None:
			self.client.stop()
			self.client.clear()
			self.client.close()
			self.client.disconnect()
			print "mpdclient -> destructor"

	def update(self):
		if self.client != None:
			self.client.update()

	def add(self, uri):
		if self.client != None:
			self.client.stop()
			self.client.clear()
			self.client.add(uri)
			self.client.play()

	def random(self, state):
		if self.client != None:
			self.client.random(state)

	def pause(self):
		if self.client != None:
			self.client.pause()
