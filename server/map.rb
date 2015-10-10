require 'thread'
require 'zlib'

require_relative 'config'
require_relative 'tile'

module Map
	$mapLock = Mutex.new
	$readCount = 0 # Tracks how many people are reading right now
	$world = Array.new

	def Map.genWorld
		$mapLock.synchronize {
			$world.clear
			# Add a new layer
			for z in (0 .. Configuration::BoardHeight - 1)
				layer = Array.new
				for y in (0 .. Configuration::BoardLength - 1)
					row = Array.new
					for x in (0 .. Configuration::BoardWidth - 1)
						row.push(Tile.new(TileType::Rock))
					end
					layer.push(row)
				end
				$world.push(layer)
			end
		}
	end

	def Map.saveState
		f = File.open(Configuration::MapFilePath, "w")
		$mapLock.synchronize {
			blob = Zlib::Deflate.deflate(Marshal.dump($world))
			f.puts(blob)
		}
		f.close
	end

	def Map.loadState
		f = File.open(Configuration::MapFilePath, "r")
		$mapLock.synchronize {
			$world = Marshal.load(Zlib::Inflate.inflate(f.read))
		}
		f.close
	end

end
