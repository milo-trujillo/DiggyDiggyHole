import socket
import threading
import time

class udpoutthread (threading.Thread):
	def __init__(self, threadID, name, ip, port, MESSAGE, sock):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.ip = ip
		self.port = port
		self.MESSAGE = MESSAGE
		self.sock = sock

	def run(self):
		print("Opening UDP thread...")
		udpsend(self.ip, self.port, self.MESSAGE, self.sock)
		print("Closing UDP thread...")

class heartbeat(threading.Thread):
	def __init__(self, UDP_IP):
		threading.Thread.__init__(self)
		self.UDP_IP = UDP_IP
		self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		self.UDP_PORT = 1392
		self.MESSAGE = "badum"
		self.paused = True
		self.state = threading.Condition()
		self.time = int(time.time())
		self.lasttime = int(time.time())

	def run(self):
		self.resume()
		while True:
			with self.state:
				if self.paused:
					self.state.wait()
			self.time = int(time.time())
			if( (self.time % 3 == 0) & (self.time != self.lasttime) ):
				udpsend( self.UDP_IP, self.UDP_PORT, self.MESSAGE, self.sock )
				self.lasttime = self.time

	def pause(self):
		with self.state:
			self.paused = True
			self.state.notify()
			print("Heart stopped.")

	def resume(self):
		with self.state:
			self.paused = False
			self.state.notify()
			print("Heart beating...")

class udplisten(threading.Thread):
	def __init__(self, UDP_IP, UDP_PORT):
		threading.Thread.__init__(self)
		self.UDP_IP = UDP_IP
		self.UDP_PORT = UDP_PORT
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.stayopen = 1

	def run(self):
		print("Listening...")
		self.sock.bind(("", self.UDP_PORT))
		while True:
			(data, addr) = self.sock.recvfrom(1024)
			print(data)
		return

def udpsend(UDP_IP, UDP_PORT, MESSAGE, outsock):
	outsock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def udprecv(UDP_IP, UDP_PORT, insock):
	insock.bind((UDP_IP, UDP_PORT))

	while True:
		(data, addr) = insock.recvfrom(1024)
		print(data)
