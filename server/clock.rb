require 'thread'

require_relative 'heartbeat'
require_relative 'config'

=begin
	This file is responsible for tracking time. Every turn duration, 
	if time is not frozen, a new turn is evaluated, which triggers effects
	throughout the game. Clock can be frozen in case we need to save state
	or there are no clients connected.
=end

module Clock
	$timeLock = Mutex.new
	$timeRunning = false
	$turns = 0

	# This function never returns and should be called in a new thread
	def Clock.tick
		puts "Tick tock..."
		while( true )
			sleep Configuration::TurnDuration
			$timeLock.synchronize {
				# If no clients are hooked up, freeze
				if( $timeRunning == false || Heartbeat.getClients == 0 )
					$timeRunning = false
					next
				end

				# Do whatever we need to do on new turns here
				Heartbeat.fade

				# Turn counter goes up!
				$turns += 1
				if( $turns % 5 == 0 )
					puts ("Turn: " + $turns.to_s)
				end
			}
		end
	end

	def Clock.start
		$timeLock.synchronize {
			$timeRunning = true
		}
	end

	def Clock.stop # It's hammer time
		$timeLock.synchronize {
			$timeRunning = false
		}
	end

	def Clock.saveState
		f = File.open(Configuration::ClockFilePath, "w")
		$timeLock.synchronize {
			f.puts($turns)
		}
		f.close
	end

	def Clock.loadState
		f = File.open(Configuration::ClockFilePath, "r")
		$timeLock.synchronize {
			$turns = f.gets.to_i
		}
		f.close
	end

	def Clock.halt
		f = File.open(Configuration::ClockFilePath, "w")
		$timeLock.synchronize {
			f.puts($turns)
			$timeRunning = false
		}
	end
end
