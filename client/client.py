#!/usr/bin/env python3

import os.path
import socket
import time
import sys
import threading


def heartbeat(UDP_IP, sock):
	#default port is 1392, "badum" is the heartbeat
	UDP_PORT = 1392
	MESSAGE = "badum"

	#sends the message
	sock.sendto( bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
	

def initialize():
	#first we want to see if there's a pre-existing config
	if( os.path.isfile("prevconfig") ):
		#we ask whether the user wants to use the previous config for the server
		response = input("Would you like to use the previous server config? [Y/N]")

		#if they don't put a Y or N in, we keep asking
		while(	( response != "Y" ) & ( response != "N" ) & 
						(	response != "y" ) & ( response != "n" )	):
			print("Invalid response, please enter Y or N.")
			response = input("Would you like to use the previous server config? [Y/N]")
		
		if( response == "Y" ):
			conffile = open("prevconfig","r")
			ip = conffile.read()
			conffile.close()
			return ip
			
		elif( response == "N" ):
			ip = input('Please enter server ip: ')
			conffile = open("prevconfig","w")
			conffile.write(ip)
			conffile.close()
			return ip
		
	#if there isn't one, we want to make one
	else:
		ip = input('Please enter server ip: ')
		conffile = open("prevconfig","w")
		conffile.write(ip)
		conffile.close()
		return ip


#main()
if __name__ == "__main__":
	
	#we ask the user what ip they want to connect to
	ip = initialize()
	print("Connecting to",ip + "...")
	#then after that we determine what the program start time is
	clientstarttime = time.time()

	#opens the socket
	heartbeatsock = socket.socket( socket.AF_INET,	socket.SOCK_DGRAM )

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
			heartbeat(ip, heartbeatsock)
		if( idletime > 1200 ):
			print("Client timeout.")
			exit(1)

