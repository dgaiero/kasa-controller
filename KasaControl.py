import argparse
import asyncio
import os
import platform
import sys
import time

from dotenv import load_dotenv
from kasa import SmartPlug
from kasa.exceptions import SmartDeviceException

from verify_ip import verify_ip


class KasaControl:

	def __init__(self, ip=None):
		self._ip = ip
		self._plug = None
		self._args = None

	def parse_args(self):
		parser = argparse.ArgumentParser(prog="kasa")
		parser.add_argument('command', choices=['on', 'off', 'status'])
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
			self._ip = os.getenv('KASA_DEVICE_IP_ADDR')
		if self._ip is None:
			self._debug(f'Invalid IP address (actual {self._ip} expected XX.XX.XX.XX)')
			sys.exit(1)
		if verify_ip(self._ip) == False:
			self._debug(f'Invalid IP address (actual {self._ip} expected XX.XX.XX.XX)')
			sys.exit(1)
		self._debug(f'ip address is set to {self._ip}', 1)

	def run_command(self):
		self._initalize_device()
		if self._args.command == 'on':
			self._on()
		elif self._args.command == 'off':
			self._off()
		elif self._args.command == 'status':
			self._status()
		else:
			print(f"command not valid (actual {self._args.command} expected one of {'on', 'off', 'status'}")

	def _initalize_device(self):
		# self._ip
		self._plug = SmartPlug(self._ip)
		self._send_command(self._plug.update())
		try:
			self._debug(f'connected to plug: {self._plug.alias}', 1)
		except SmartDeviceException:
			self._failure()

	def _on(self):
		self._send_command(self._plug.turn_on())
		if self._verify_state(True):
			self._debug('device is turned on', 1)
		else:
			self._debug('device failed to turn on')

	def _off(self):
		self._send_command(self._plug.turn_off())
		if self._verify_state(False):
			self._debug('device is turned off', 1)
		else:
			self._debug('device failed to turn off')

	def _status(self):
		if self._verify_state(True):
			self._debug('device is turned on', 0)
		else:
			self._debug('device is turned off', 0)

	def _send_command(self, cmd):
		try:
			asyncio.run(cmd)
		except SmartDeviceException:
			self._failure()

	def _verify_state(self, state):
		self._send_command(self._plug.update())
		return self._plug.is_on == state

	def _debug(self, msg, level=0):
		if level <= self._args.verbose:
			print("-"*level, end="")
			print(msg)

	def _failure(self):
		self._debug(f'failed to communicate with the device at {self._ip}')
		sys.exit(1)

def main():
	device = KasaControl()
	device.parse_args()
	device.run_command()

if __name__ == "__main__":
	main()
