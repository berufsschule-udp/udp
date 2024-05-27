from datetime import datetime
from logging import DEBUG, ERROR, FATAL, FileHandler, Formatter, INFO,\
	StreamHandler, WARNING,	basicConfig, getLogger
from sys import stdout
from typing import TYPE_CHECKING
from gateway.env import log_dir, log_level

if TYPE_CHECKING:
	from typing import Callable

def init_logger():
	if not log_level():
		getLogger().disabled = True
		return

	getLogger().setLevel(log_level())
	getLogger().addHandler(get_stream_handler())
	if log_dir(): getLogger().addHandler(get_file_handler())

	basicConfig(encoding='utf-8', level=log_level())

def get_stream_handler():
	stream_handler = StreamHandler(stdout)
	stream_handler.setLevel(log_level())
	stream_handler.setFormatter(Formatter(
		'%(asctime)s %(levelname)s: %(message)s', '%H:%M:%S'
	))
	return stream_handler

def get_file_handler():
	file_handler = FileHandler(
		f'{log_dir()}{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log'
	)
	file_handler.setLevel(ERROR)
	file_handler.setFormatter(Formatter(
		'%(asctime)s %(levelname)s: %(message)s'
	))
	return file_handler

def log(message: 'Callable', level: int):
	if getLogger().level <= level:
		getLogger().log(level, message())

def trace(message: 'Callable'):
	log(message, DEBUG)

def info(message: 'Callable'):
	log(message, INFO)

def warn(message: 'Callable'):
	log(message, WARNING)

def error(message: 'Callable'):
	log(message, ERROR)

def fatal(message: 'Callable'):
	log(message, FATAL)