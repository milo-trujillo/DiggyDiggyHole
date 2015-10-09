require 'thread'

=begin
	This file stores configuration constants for the whole server
=end

Thread.abort_on_exception = true

module Configuration

	# All constants about size or quantity of objects
	DefaultDwarves = 7

	# All timers or time related constants
	TurnDuration = 1        # How many seconds per turn
	ClientTimeout = 10      # How many seconds until client is purged

	# Networking constants
	BindAddress = "0.0.0.0" # Bind to all addresses
	BindPort = 1392         # "DiggyDiggyHole" ascii values added together
	MaxMessageLength = 512  # Maximum byte size of any message

	# Threading constants (sizes of threadpools)
	MessageWorkers = 3      # How many threads should handle messages

	# Paths
	StateDir = "./state"
	ClockFilePath = StateDir + "/time.db"
	DwarfFilePath = StateDir + "/dwarves.db"
	StateFiles = [ClockFilePath, DwarfFilePath]

	###
	### Everything below this point is for the handling of configuration and
	### state files. Any hardcoded configuration should be above.
	###

	def Configuration.prepareState
		unless( File.directory?(StateDir) )
			begin
				Dir.mkdir(StateDir)
			rescue
				puts "Error making state directory!"
				return false
			end
			return true
		end
		return true
	end

	def Configuration.stateExists?
		for f in StateFiles
			unless( File.exists?(f) )
				return false
			end
		end
		return true
	end

	def Configuration.clearState
		for f in StateFiles
			if( File.exists?(f) )
				begin
					File.delete(f)
				rescue
					puts "Warning: unable to delete file '" + f + "'!"
				end
			end
		end
	end

end
