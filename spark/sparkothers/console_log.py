#!/usr/bin/python3
import sys


class ConsoleLog:
	def __init__(self, enable_log=False, log_name=None):
		self.log_name = log_name
		self.enable_log = enable_log

		self.error_color = '\033[1;40;31m'
		self.info_color = '\033[1;40;32m'
		self.warn_color = '\033[1;40;33m'
		self.caller_name_color = '\033[1;40;34m'
		self.log_name_color = '\033[1;40;35m'
		self.debug_color = '\033[1;40;36m'
		self.normal_color = '\033[1;40;37m'
		self.end_color = '\033[0m'

		self.clear()

	def clear(self):
		if self.enable_log:
			print("\033c", end="console was cleared\n")
#		pass

	def __log__(self, caller_name, message):
		message =  ' '.join(map(str, message))
		caller = sys._getframe(1).f_code.co_name

		if hasattr(self, f"{caller}_color"):
			color = getattr(self, f"{caller}_color")
		else:
			color = None
		if self.enable_log:
			if self.log_name != None:
				print(f"{self.log_name_color}{self.log_name}{self.end_color}:" ,
						f"{self.caller_name_color}{caller_name}{self.end_color}:" ,
						f"{color}{caller.upper()}{self.end_color}:",
						message
					)
			else:
				print(f"{self.caller_name_color}{caller_name}{self.end_color}:" ,
						f"{color}{caller.upper()}{self.end_color}:",
						message
					)
		if not self.enable_log:
			if caller == "normal":
				print(f"{message}")

	def normal(self, *args):
		caller_name = sys._getframe(1).f_code.co_name
		self.__log__(caller_name, args)

	def info(self, *args):
		caller_name = sys._getframe(1).f_code.co_name
		self.__log__(caller_name, args)

	def warn(self, *args):
		caller_name = sys._getframe(1).f_code.co_name
		self.__log__(caller_name, args)

	def error(self, *args):
		caller_name = sys._getframe(1).f_code.co_name
		self.__log__(caller_name, args)

	def debug(self, *args):
		caller_name = sys._getframe(1).f_code.co_name
		self.__log__(caller_name, args)


if __name__ == "__main__":
	log = ConsoleLog(True)
#	log.log_name= __file__+__name__
	log.normal("normal")
	log.info("info")
	log.warn("warn")
	log.error("error")
	log.debug("debug")



