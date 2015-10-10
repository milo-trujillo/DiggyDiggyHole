require_relative 'config'

=begin

=end

module TileType
	Rock = 0
	Air = 1

	Types = [Rock, Air]
end

class Tile
	attr_accessor :type

	def initialize(t)
		@type = nil
		for type in TileType::Types
			if( t == type )
				@type = t
			end
		end
		if( @type == nil )
			raise IllegalType, "Invalid tile type!"
		end
	end
end
