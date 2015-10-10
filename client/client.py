#!/usr/bin/env python3

import select
import os.path
from os import _exit
import socket
import time
import sys
import threading
import udp


	

def initialize():
	conffilename = "prevconfig.conf"
	#first we want to see if there's a pre-existing config
	if( os.path.isfile(conffilename) ):
		#we ask whether the user wants to use the previous config for the server
		response = input("Would you like to use the previous server config? [Y/N]")

		#if they don't put a Y or N in, we keep asking
		while(	( response.lower() != "yes" ) & ( response.lower() != "no" ) & 
						(	response.lower() != "y" ) & ( response.lower() != "n" )	):
			print("Invalid response, please enter Y or N.")
			response = input("Would you like to use the previous server config? [Y/N]")
		
		#if they want to use their previous config, we load that
		if( ( response.lower() == "y") | (response.lower() == "yes" ) ):
			conffile = open(conffilename,"r")
			ip = conffile.read()
			conffile.close()
			return ip
		
		#otherwise we ask for a new ip to use
		elif( ( response.lower() == "n" ) | ( response.lower() == "no" ) ):
			ip = input('Please enter server ip: ')
			conffile = open(conffilename,"w")
			conffile.write(ip)
			conffile.close()
			return ip
		
	#if there isn't one, we want to make one
	else:
		ip = input('Please enter server ip: ')
		conffile = open(conffilename,"w")
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

	UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	UDPsock.bind(('',1392))
	
	#create the thread for the heartbeat
	heartbeatthread = udp.heartbeat( ip, UDPsock )
	listenthread = udp.udplisten( UDPsock )

	heartbeatthread.start()
	listenthread.start()

	while (1):
		meme = UDPsock.recvfrom(1024)
		print(meme[0])
		#because it is used multiple times, there's no reason to continue
		#to call the time function, so instead it is just stored into a
		#variable at the beginning of the while loop
		currenttime = time.time()

		#this will be replaced eventually, and there'll be some way to
		#determine user activity
		idletime = currenttime - clientstarttime

		#Heartbeat function runs every 3 seconds this way.
		if( idletime > 1200 ):
			heartbeatthread.pause()
			close = input("Would you like to continue?[Y/N]")
			while( (close.lower() != "n") & (close.lower() != "y")
							& (close.lower() != "yes") & (close.lower() != "no") ):
				close = input("Invalid input.\nWould you like to continue?[Y/N]")
			if( (close.lower() == "n") | (close.lower() == "no") ):
				print("Client timeout.")
				os._exit(0)
			else:
				heartbeatthread.resume()
				clientstarttime = time.time()
