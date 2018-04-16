"""Simple Implementation of an Artnet receiver.

Python Version: 3.6
Source: http://artisticlicence.com/WebSiteMaster/User%20Guides/art-net.pdf
		http://art-net.org.uk/wordpress/structure/streaming-packets/artdmx-packet-definition/

NOTES
- For simplicity: Did not implement NET or SUBNET, these default to 0

TODO
- Parsing with memory view:
	https://docs.python.org/3/library/stdtypes.html#memoryview
	https://eli.thegreenplace.net/2011/11/28/less-copies-in-python-with-the-buffer-protocol-and-memoryviews

"""

import socket
import datetime

class StupidArtnetServer():
	"""(Very) simple implementation of an Artnet receiver."""

	UDP_PORT = 6454
	bIsListening = False
	buffer_size = 600

	def __init__(self, universe=0):
		"""Class Initialization."""
		# Instance variables
		self.UNIVERSE = universe
		self.buffer = bytearray(self.buffer_size)

		self.bIsListening = True

	def __str__(self):
		"""Printable object state."""
		s = "==================================="
		s = "Stupid Artnet Receiver initialized\n"
		s += "Listening for Universe: %i \n" % self.UNIVERSE

		return s

	def close(self):
		"""Close UDP socket."""
		self.s.detach()

	##
	# SOCKET
	##

	def start(self):
		"""Start Listening to Artnet."""
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind(('localhost', self.UDP_PORT))

		while (self.bIsListening):
			data = s.recv_into(self.buffer)
			if not data:
				continue
			u, p = self.parse_packet()
			if (u > -1):
				print('{} Got Art-Net on Universe {} Packet Size {}'.format(datetime.datetime.now(), u, p))
		print('Connection closed')

	def parse_packet(self):
		"""Parse data in buffer."""
		if (len(self.buffer) < 20):	# 18 being the header size of a DMX packet
			print('Unknow data')
			return (-1, -1)

		data = memoryview(self.buffer)		# Create memory view

		# 1 - Check if it is artnet
		if (data[:7] != b'Art-Net'):
			print(self.buffer.decode())
			print('Unknow data')
			return (-1, -1)

		# Next we should have an empty byte, we skip it

		# 2 - And the packet description (opcode)
		# We only implement Art-Dmx here
		if (data[9] != 0x50):
			print(self.buffer[9].decode())
			print('Not ArtDmx')
			return (-1, -1)

		# 3 - Double check protocol version
		if (data[11] != 14):
			print('ERROR: protocol version {}: proceeding either way'.format(data[11]))

		# We skip sequence here

		# 4 - Read Universe - data[14] LOW - data[15] HIGH
		universe = self.shift_back(data[14], data[15])

		# 5 - Read Packet Size - data[16] HIGH - data[17] LOW
		packet_size = self.shift_back(data[17], data[16])

		return (universe, packet_size)

	def stop(self):
		"""Stop Listening to Artnet."""
		self.bIsListening = False
		self.close()

	##
	# SETTERS - HEADER
	##

	def set_universe(self, universe):
		"""Setter for universe."""
		self.UNIVERSE = universe
		v = self.shift_this(self.UNIVERSE)
		self._unL = v[1]
		self._unH = v[0]

	def set_physical(self, physical):
		"""Setter for physical address.

		Not implemented
		"""
		self.PHYSICAL = physical  # not implemented

	def set_net(self, net):
		"""Setter for net address.

		Not implemented
		"""
		self.NET = net  # not implemented

	##
	# UTILS
	##

	@staticmethod
	def shift_this(number, high_first=True):
		"""Utility method: extracts MSB and LSB from number.

		Defaults to returning high byte first"""
		low = (number & 0xFF)
		high = ((number >> 8) & 0xFF)
		if (high_first):
			return((high, low))
		else:
			return((low, high))
		print("Something went wrong")
		return False

	@staticmethod
	def shift_back(low, high):
		"""Utility method: extracts number from  MSB and LSB.

		Use low byte first"""
		return (low | (high << 8))

	@staticmethod
	def put_in_range(number, range_min, range_max, make_even=True):
		"""Utility method: sets number in defined range."""
		if (make_even and number % 2 != 0):
			number += 1
		if (number < range_min):
			number = range_min
		if (number > range_max):
			number = range_max
		return number


class StupidArtnetFixture(StupidArtnetServer):
	"""Fixture listens to single channel in given address."""

	def __init__(channel, universe=0):
		"""Initialize instance."""
		self.set_channel(channel)
		self.set_universe(universe)

	##
	# SETTERS
	##

	def set_channel(self, channel):
		"""Set Listenning channel."""
		self.channel = put_in_range(channelr, 1, 512, False)

	def set_universe(self, universe):
		"""Set Listening Universe."""
		self.universe = universe
		u = shift_this(universe)
		self._unH = u[0]
		self._unL = u[1]
		print("Universe Set to {}".format(universe))

	##
	# GETTERS
	##

	def get_value():
		"""."""
		pass

if __name__ == '__main__':
	import time

	print("===================================")
	print("Namespace run")

	universe = 0 					# see docs
	a = StupidArtnetServer()
	print(a)
	a.start()
