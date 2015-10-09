require 'thread'
require 'socket'

require_relative 'config'

=begin
	This module is for tracking which clients have recently talked to us.

	This is important for two reasons:
		* We want to freeze time when no one is playing
		* We use this list to know who to send game updates to

	One thread should be dedicated to Heartbeat.updateClients, which will send
	update messages about the game to all connected clients.
=end

module Heartbeat
	$clients = Hash.new
	$heartLock = Mutex.new
	$updates = Queue.new

	# Returns the number of clients
	def Heartbeat.getClients
		$heartLock.synchronize {
			return $clients.size
		}
	end

	# This should be called each time we receive a heartbeat message
	def Heartbeat.heardFrom(host)
		$heartLock.synchronize {
			$clients[host] += 1
		}
	end

	# This is called once per turn
	def Heartbeat.fade
		$heartLock.synchronize {
			$clients.each_key {|host| $clients[host] += 1}
			$clients.delete_if {|host, time| time >= Configuration::ClientTimeout}
		}
	end

	# This is called externally to post new messages to send to all clients
	def Heartbeat.addUpdate(update)
		$updates << update
	end

	# This should be called *once* on a dedicated thread
	def Heartbeat.updateClients
		u = UDPSocket.new
		u.bind(Configuration::BindAddress, Configuration::BindPort)
		puts "Ready to send updates."
		while(true)
			update = $updates.pop
			$heartLock.synchronize {
				for client in $clients
					u.send(update, 0, client[0], client[1])
				end
			}
		end
	end
end
