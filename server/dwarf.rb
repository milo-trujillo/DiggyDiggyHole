require_relative 'config'

=begin
	Dwarves! They're smelly and like alcohol!

	This class stores information about a dwarf and its little
	dwarven state. For now this means where the dwarf is and what they're up to. 

	Later it will also include all dwarven AI.
=end

class Dwarf
	attr_reader :x, :y, :z, :name, :task
	Idle = "Idle"

	def initialize(x, y, z)
		@x = x
		@y = y
		@z = z
		@name = "Foo" # Later they'll auto-gen names
		@task = Idle
	end

	def chooseRandomTask()
		@task = Idle
	end

	def work()
		if( @task == Idle )
			@task = chooseRandomTask
		end
	end
end
