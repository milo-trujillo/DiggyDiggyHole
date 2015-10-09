require 'thread'
require 'zlib'

require_relative 'config'
require_relative 'dwarf'

=begin
	This module tracks and controls all dwarves. This is the module you
	should import and use, *not* dwarf.rb.
=end

module Dwarves
	$dwarfLock = Mutex.new
	$dwarves = Array.new

	def Dwarves.spawn(num)
		$dwarfLock.synchronize {
			for x in (0 .. num - 1)
				$dwarves.push(Dwarf.new(0,0,0))
			end
		}
	end

	def Dwarves.saveState
		f = File.open(Configuration::DwarfFilePath, "w")
		$dwarfLock.synchronize {
			d = Zlib::Deflate.deflate(Marshal.dump($dwarves))
			f.puts(d)
		}
		f.close
	end

	def Dwarves.loadState
		f = File.open(Configuration::DwarfFilePath, "r")
		$dwarfLock.synchronize {
			$dwarves = Marshal.load(Zlib::Inflate.inflate(f.read))
		}
		f.close
	end

	def Dwarves.handleDwarves
		$dwarfLock.synchronize {
			for d in $dwarves
				# Handle dwarfy behavior here
			end
		}
	end
end
