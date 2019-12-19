import logging
#--------------------------------------------------------------------------------------------------

def loggingleval(leval):
	if leval == 'INFO':
		return logging.INFO

	elif leval == 'WARNING':
		return logging.WARNING

	elif leval == 'ERROR':
		return logging.ERROR

	elif leval == 'CRITICAL':
		return logging.CRITICAL

	elif leval == 'DEBUG':
		return logging.DEBUG
	else:
		return logging.DEBUG


class LoggingFormatter(logging.Formatter):
	console_fmt = logging.Formatter('%(name)s : %(levelname)s : %(message)s')
	#info_fmt = logging.Formatter('%(levelname)s : %(message)s')
	def format(self, record):
		if record.levelno == logging.DEBUG:
			record.msg = '\033[96m%s\033[0m' % record.msg
			return self.console_fmt.format(record)
		if record.levelno == logging.CRITICAL:
			record.msg = '\033[94m%s\033[0m' % record.msg
			return self.console_fmt.format(record)
		elif record.levelno == logging.ERROR:
			record.msg = '\033[91m%s\033[0m' % record.msg
			return self.console_fmt.format(record)
		if record.levelno == logging.WARNING:
			record.msg = '\033[93m%s\033[0m' % record.msg
			return self.console_fmt.format(record)
		elif record.levelno == logging.INFO:
			record.msg = '\033[92m%s\033[0m' % record.msg
			return self.console_fmt.format(record)
class Logging:
	def __init__(self,  name=__name__, logger_type='console', log_file=__name__+'.log', leval='DEBUG', state=True):
		self.name = name
		self.logger_type = logger_type
		self.file_name = log_file
		self.state = state
		self.leval = leval
		file_fmt = ('%(asctime)s :%(name)s : %(levelname)s : %(message)s')
		self.logger = logging.getLogger(self.name)
		self.logger.setLevel(loggingleval(self.leval))
		if self.logger_type == "console":
			self.console_handler = logging.StreamHandler()
			self.console_handler.setLevel(loggingleval(self.leval))
			self.console_formatter = LoggingFormatter()
			self.console_handler.setFormatter(self.console_formatter)
			self.logger.addHandler(self.console_handler)
		elif self.logger_type == "file":
			self.file_handler = logging.FileHandler(self.file_name )
			self.file_handler.setLevel(loggingleval(self.leval))
			self.file_formatter = logging.Formatter(file_fmt)
			self.file_handler.setFormatter(self.file_formatter)
			self.logger.addHandler(self.file_handler)
		elif self.logger_type == "both":
			self.file_handler = logging.FileHandler(self.file_name )
			self.file_handler.setLevel(loggingleval(self.leval))
			self.file_formatter = logging.Formatter(file_fmt)
			self.file_handler.setFormatter(self.file_formatter)
			self.logger.addHandler(self.file_handler)
			self.console_handler = logging.StreamHandler()
			self.console_handler.setLevel(loggingleval(self.leval))
			self.console_formatter =  LoggingFormatter()
			self.console_handler.setFormatter(self.console_formatter)
			self.logger.addHandler(self.console_handler)
		#else :
			#self.state = False
		if self.state == True:
			print('Logging ON for %s type %s leval %s' %(name, self.logger_type, self.leval))
		else :
			self.state = False
			print('Logging OFF for %s' %(self.name))
	def info(self, message = ''):
		if self.state == True:
			self.logger.info(message)
	def warning(self, message):
		if self.state ==  True:
			self.logger.warning(message)
	def error(self, message):
		if self.state ==  True:
			self.logger.error(message)
	def critical(self, message):
		if self.state ==  True:
			self.logger.critical(message)
	def debug(self, message):
		if self.state ==  True:
			self.logger.debug(message)

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	#  XXX 'application' code
	log = Logging()
	log.info('info message')
	log.warning('warning message')
	log.error('error message')
	log.critical('critical message')
	log.debug('debug message')


