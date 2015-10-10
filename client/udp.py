import socket
import threading
import time
import select

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

#specifically for letting the server know you're still connected
class heartbeat(threading.Thread):
	def __init__(self, ip, sock):
		threading.Thread.__init__(self)
		#server address is a tuple of its ip and port to talk to
		self.server = (ip, 1392)
		#socket is passed in as an argument
		self.sock = sock
		#the heartbeat message
		self.MESSAGE = "badum"
		#used for pausing the heartbeat, e.g. for inactivity
		self.paused = True
		#weird stuff, google said so
		self.state = threading.Condition()
		#for determining how often to sent the message
		self.time = int(time.time())
		self.lasttime = int(time.time())
	#startup code for thread
	def run(self):
		#it starts out paused, so we unpause it
		self.resume()
		while True:
			#this bit allows me to pause it if i want to
			with self.state:
				if self.paused:
					self.state.wait()
			#we want to send every 3 seconds, and make sure we arent sending too much
			self.time = int(time.time())
			if( (self.time % 3 == 0) & (self.time != self.lasttime) ):
				self.sock.sendto( bytes(self.MESSAGE, "utf-8"), (self.server))
				self.lasttime = self.time

	def pause(self):
		#weird stuff to pause it
		with self.state:
			self.paused = True
			self.state.notify()
			print("Heart stopped.")

	def resume(self):
		#weird stuff to resume it
		with self.state:
			self.paused = False
			self.state.notify()
			print("Heart beating...")

class udplisten(threading.Thread):
	def __init__(self, sock):
		threading.Thread.__init__(self)
		self.sock = sock

	def run(self):
		print("Listening...")
		while True:
			#receive on the socket, and decode the message
			turn = self.sock.recvfrom(1024)
			print(turn[0].decode("utf-8"))

def udpsend(UDP_IP, UDP_PORT, MESSAGE, outsock):
	outsock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def udprecv(UDP_IP, UDP_PORT, insock):
	insock.bind((UDP_IP, UDP_PORT))

	while True:
		(data, addr) = insock.recvfrom(1024)
		print(data)
