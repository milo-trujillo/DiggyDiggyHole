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
	def __init__(self, threadID, name, UDP_IP, sock):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.UDP_IP = UDP_IP
		self.sock = sock
		self.UDP_PORT = 1392
		self.MESSAGE = "badum"
		self.stayopen = 1
		self.starttime = time.time()

	def run(self):
		print("Heart beating...")
		while(self.stayopen):
			if( self.starttime % 3 == 0 ):
				self.sock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
		print("Heart stopped.")
		return
	def close(self):
		self.stayopen = 0
		return

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
		while(self.stayopen):
			(data, addr) = self.sock.recvfrom(1024)
			print(data)
		print("No longer listening.")
		return

	def close(self):
		self.stayopen = 0
		return


def udpsend(UDP_IP, UDP_PORT, MESSAGE, outsock):
	outsock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def udprecv(UDP_IP, UDP_PORT, insock):
	insock.bind((UDP_IP, UDP_PORT))

	while True:
		(data, addr) = insock.recvfrom(1024)
		print(data)
