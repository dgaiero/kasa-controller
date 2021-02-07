import argparse
import asyncio
import time
import os
import sys
from dotenv import load_dotenv
from kasa import SmartPlug
from verify_ip import verify_ip



# plug = SmartPlug('172.16.15.85')
# asyncio.run(plug.update())

# asyncio.run(plug.turn_on())
# time.sleep(10)
# asyncio.run(plug.turn_off())

class LightControl:

	def __init__(self, ip=None):
		self._ip = ip
		self._plug = None
		self._args = None

	def parse_args(self):
		parser = argparse.ArgumentParser(prog="light")
		parser.add_argument('command', choices=['on', 'off'])
		parser.add_argument('--verbose', '-v', action='count', default=0)
		parser.add_argument('-ip', help='IP address of smart plug', default=None)
		self._args = parser.parse_args()
		self._debug(self._args, 3)
		self._debug('debug level only goes to 3 (-vvv)', 4)
		if hasattr(self._args, 'ip') and self._args.ip is not None:
			self._debug('loading ip from sys.argv', 3)
			self._ip = self._args.ip
		else:
			self._debug('loading ip from environment', 3)
			load_dotenv()
			self._ip = os.getenv('LIGHT_CONTROL_IP_ADDR')
		if verify_ip(self._ip) == False:
			self._debug(f'Invalid IP address (actual {self._ip} expected XX.XX.XX.XX)')
			sys.exit()
		self._debug(f'ip address is set to {self._ip}', 1)

	def run_command(self):
		self._initalize_device()
		if self._args.command == 'on':
			self._on()
		else:
			self._off()

	def _initalize_device(self):
		# self._ip
		self._plug = SmartPlug(self._ip)
		asyncio.run(self._plug.update())
		self._debug(f'connected to plug: {self._plug.alias}', 1)

	def _on(self):
		asyncio.run(self._plug.turn_on())
		if self._verify_state(True):
			self._debug('plug is turned on', 1)
		else:
			self._debug('plug failed to turn on')

	def _off(self):
		asyncio.run(self._plug.turn_off())
		if self._verify_state(False):
			self._debug('plug is turned off', 1)
		else:
			self._debug('plug failed to turn off')

	def _verify_state(self, state):
		asyncio.run(self._plug.update())
		return self._plug.is_on == state

	def _debug(self, msg, level=0):
		if level <= self._args.verbose:
			print("-"*level, end="")
			print(msg)

def main():
	light = LightControl()
	light.parse_args()
	light.run_command()

if __name__ == "__main__":
	main()
