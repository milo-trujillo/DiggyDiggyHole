#!/usr/bin/env ruby

require 'thread'

require_relative 'config'
require_relative 'clock'
require_relative 'heartbeat'
require_relative 'dwarves'
require_relative 'messages'

SIGNAL_QUEUE = []
[:INT, :TERM].each do |signal|
	Signal.trap(signal) do
		SIGNAL_QUEUE << signal
	end
end

def handleInt
	puts ""
	puts "Saving state..."
	Configuration.prepareState()
	puts "State dir ready"
	Clock.halt
	puts "Clock halted"
	Dwarves.saveState
	puts "Dwarves saved"
	puts "Quitting..."
	exit(0)
end

if $0 == __FILE__
	puts "Starting game server..."
	if( Configuration.stateExists? )
		puts "Found existing hole..."
		Clock.loadState
		Dwarves.loadState
	else
		puts "Digging a new hole..."
		Dwarves.spawn(Configuration::DefaultDwarves)
	end

	# Start off server processes
	Thread.start do Clock.tick end # Time keeps on ticking...
	Thread.start do Heartbeat.updateClients end
	for x in (0 .. Configuration::MessageWorkers - 1)
		Thread.start do Messages.handle end
	end
	Thread.start do Messages.listen end

	# At this point the main thread is really just here so that
	# we're attached to a terminal for logging, and so we can
	# intercept the eventual ^C.
	while(true)
		sig = SIGNAL_QUEUE.pop
		if( sig == :INT )
			handleInt
		end
	end
end
