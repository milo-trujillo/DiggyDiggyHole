require 'socket'

require_relative 'config'
require_relative 'heartbeat'

=begin
	This module is responsible for receiving all messages from clients,
	interpreting those messages, and running the appropriate code.

	It has one thread receiving messages and stuffing them on a queue, where
	a threadpool then processes each new task.

	One thread should be dedicated to Messages.listen.
	One or more threads should be dedicated to Messages.handle, which does
	the actual interpretation.

	Note: Sending update messages back to the client is done in 'heartbeat'
=end

module Messages
	$messages = Queue.new

	def Messages.listen
		u = UDPSocket.new
		u.bind(Configuration::BindAddress, Configuration::BindPort)
		while(true)
			(msg, hostData) = u.recvfrom(Configuration::MaxMessageLength)
			$messages << [msg, [hostData[3], hostData[1]]]
		end
	end

	def Messages.handle
		while(true)
			(msg, host) = $messages.pop
			if( msg == "badum" )
				Heartbeat.heardFrom(host)
			end
		end
	end

end
