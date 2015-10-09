import socket
import time
import sys


def heartbeat(UDP_IP):
	#default port is 1392, "badum" is the heartbeat
	UDP_PORT = 1392
	MESSAGE = "badum"

	#opens the socket
	sock = socket.socket( socket.AF_INET,	socket.SOCK_DGRAM )
	#sends the message
	sock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
	



#main()
if __name__ == "__main__":

	#we ask the user what ip they want to connect to
	ip = input('Please enter ip: ')

	#then after that we determine what the program start time is
	clientstarttime = time.time()

	while (1):

		#because it is used multiple times, there's no reason to continue
		#to call the time function, so instead it is just stored into a
		#variable at the beginning of the while loop
		currenttime = time.time()

		#this will be replaced eventually, and there'll be some way to
		#determine user activity
		idletime = currenttime - clientstarttime

		#Heartbeat function runs every 3 seconds this way.
		if( ( (currenttime % 3 ) == 0 ) & ( idletime <= 1200) ):
			heartbeat(ip)

