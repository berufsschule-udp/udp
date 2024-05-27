from functools import cache
from os import environ

def init_env():
	from dotenv import load_dotenv
	load_dotenv()

@cache
def log_level():
	return {
		'': None,
		'trace': 10,
		'info': 20,
		'warn': 30,
		'error': 40,
		'fatal': 50
	}[environ.get('LOG_LEVEL')]

@cache
def log_dir():
	return environ.get('LOG_DIR')

@cache
def log_frames():
	return environ.get('LOG_FRAMES')

@cache
def log_sql():
	return environ.get('LOG_SQL')

@cache
def multicast_ip_and_port():
	ip, port = tuple(environ.get('MULTICAST').split(':'))
	return ip, int(port)

@cache
def nics():
	return environ.get('NICS').split()

@cache
def channels_role_and_indexes():
	roles_and_indexes: list[tuple[str, int]] = []

	for channel in environ.get('CHANNELS').split():
		role, *indexes = channel.split('.')
		roles_and_indexes.extend((role, i) for i in map(int, indexes))

	return roles_and_indexes

@cache
def channel_values_count():
	return int(environ.get('CHANNELS_VALUES_COUNT'))

@cache
def channel_max_frames_per_second():
	return int(environ.get('CHANNELS_MAX_FRAMES_PER_SECOND'))

@cache
def intervals():
	return [int(i) for i in environ.get('INTERVALS').split()]

@cache
def timestamp_check():
	return bool(environ.get('TIMESTAMP_CHECK'))

@cache
def database_enabled():
	return bool(environ.get('DATABASE_ENABLED'))

@cache
def database_connection_string():
	return environ.get('DATABASE_CONNECTION_STRING')