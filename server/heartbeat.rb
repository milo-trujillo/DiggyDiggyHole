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

	One thread should be dedicated to Heartbeat.handleBeats, which will update
	the list of clients appropriately as new heartbeats come in.
=end

module Heartbeat
	$clients = Hash.new
	$heartLock = Mutex.new
	$heartSizeLock = Mutex.new
	$updates = Queue.new
	$newBeats = Queue.new
	$size = 0

	# Returns the number of clients
	def Heartbeat.getClients
		$heartSizeLock.synchronize {
			return $size
		}
	end

	def Heartbeat.handleBeats()
		while(true)
			host = $newBeats.pop
			$heartLock.synchronize {
				start = false
				if( $clients.empty? )
					start = true
				end
				$clients[host] = 0
				$heartSizeLock.synchronize {
					$size += 1
				}
				if( start )
					Clock.start
				end
			}
		end
	end

	# This should be called each time we receive a heartbeat message
	def Heartbeat.heardFrom(host)
		$newBeats << host
	end

	# This is called once per turn
	def Heartbeat.fade
		$heartLock.synchronize {
			$clients.each_key {|host| $clients[host] += 1}
			$clients.delete_if {|host, time| time >= Configuration::ClientTimeout}
			$heartSizeLock.synchronize {
				$size = $clients.size
			}
		}
	end

	# This is called externally to post new messages to send to all clients
	def Heartbeat.addUpdate(update)
		$updates << update
	end

	# This should be called *once* on a dedicated thread
	def Heartbeat.updateClients
		u = UDPSocket.new
		u.bind(Configuration::BindAddress, 0)
		puts "Ready to send updates."
		while(true)
			update = $updates.pop
			clients = nil
			$heartLock.synchronize {
				clients = $clients.clone # Make a shallow copy
			}
			for c in clients
				host = c[0][0].to_s
				port = c[0][1].to_i
				# For debugging
				puts "Sending to " + host + " on port " + port.to_s
				u.send(update, 0, host, port)
			end
		end
	end
end
