import socket
import time


def heartbeat(ip):
	UDP_IP = ip
	UDP_PORT = 1392
	MESSAGE = "badum"

	print(MESSAGE)
	
	sock = socket.socket( socket.AF_INET,
												socket.SOCK_DGRAM )
	sock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
	




if __name__ == "__main__":
	ip = input('Please enter ip: ')
	while (1):

#Heartbeat function runs every 3 seconds this way.
		if((time.time() % 3) == 0):
			heartbeat(ip)
