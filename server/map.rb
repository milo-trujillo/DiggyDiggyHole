require 'thread'

module Map
	$mapLock = Mutex.new
	$readCount = 0 # Tracks how many people are reading right now

end
