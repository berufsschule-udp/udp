from os import environ
from unittest import TestCase, main
from gateway.env import channel_max_frames_per_second, channel_values_count, \
	channels_role_and_indexes, database_connection_string, database_enabled, \
	intervals, log_dir, log_frames, log_level, log_sql, \
	multicast_ip_and_port, nics, timestamp_check

class TestEnv(TestCase):
	def test_log_level_when_not_set(self):
		environ['LOG_LEVEL'] = ''
		value = log_level()
		log_level.cache_clear()
		self.assertIsNone(value)

	def test_log_level_when_set(self):
		environ['LOG_LEVEL'] = 'info'
		value = log_level()
		log_level.cache_clear()
		self.assertEqual(20, value)

	def test_log_dir(self):
		environ['LOG_DIR'] = 'path/to/log/dir'
		value = log_dir()
		log_dir.cache_clear()
		self.assertEqual('path/to/log/dir', value)

	def test_log_frames_when_true(self):
		environ['LOG_FRAMES'] = 'true'
		value = log_frames()
		log_frames.cache_clear()
		self.assertTrue(value)

	def test_log_frames_when_false(self):
		environ['LOG_FRAMES'] = ''
		value = log_frames()
		log_frames.cache_clear()
		self.assertFalse(value)

	def test_log_sql_when_true(self):
		environ['LOG_SQL'] = 'true'
		value = log_sql()
		log_sql.cache_clear()
		self.assertTrue(value)

	def test_log_sql_when_false(self):
		environ['LOG_SQL'] = ''
		value = log_sql()
		log_sql.cache_clear()
		self.assertFalse(value)

	def test_multicast_ip_and_port(self):
		environ['MULTICAST'] = '12.3.4.5:6789'
		ip, port = multicast_ip_and_port()
		multicast_ip_and_port.cache_clear()
		self.assertEqual(('12.3.4.5', 6789), (ip, port))

	def test_nics(self):
		environ['NICS'] = '12.3.4.5'
		value = nics()
		nics.cache_clear()
		self.assertEqual(['12.3.4.5'], value)

	def test_channels_role_and_indexes(self):
		environ['CHANNELS'] = 'vA1 vB2.1 vC3.0.1'
		value = channels_role_and_indexes()
		channels_role_and_indexes.cache_clear()

		self.assertEqual([('vA1', 0), ('vB2', 1), ('vC3', 0), ('vC3', 1)],
			value)

	def test_channel_values_count(self):
		environ['CHANNELS_VALUES_COUNT'] = '12'
		value = channel_values_count()
		channel_values_count.cache_clear()
		self.assertEqual(12, value)

	def test_channel_max_frames_per_second(self):
		environ['CHANNELS_MAX_FRAMES_PER_SECOND'] = '32'
		value = channel_max_frames_per_second()
		channel_max_frames_per_second.cache_clear()
		self.assertEqual(32, value)

	def test_intervals_duration_when_one(self):
		environ['INTERVALS'] = '2'
		value = intervals()
		intervals.cache_clear()
		self.assertEqual([2], value)

	def test_intervals_duration_when_many(self):
		environ['INTERVALS'] = '2 60 900'
		value = intervals()
		intervals.cache_clear()
		self.assertEqual([2, 60, 900], value)

	def test_timestamp_check_when_enabled(self):
		environ['TIMESTAMP_CHECK'] = 'true'
		value = timestamp_check()
		timestamp_check.cache_clear()
		self.assertTrue(value)

	def test_timestamp_check_when_disabled(self):
		environ['TIMESTAMP_CHECK'] = ''
		is_check = timestamp_check()
		timestamp_check.cache_clear()
		self.assertFalse(is_check)

	def test_database_enabled_when_enabled(self):
		environ['DATABASE_ENABLED'] = 'true'
		value = database_enabled()
		database_enabled.cache_clear()
		self.assertTrue(value)

	def test_database_enabled_when_disabled(self):
		environ['DATABASE_ENABLED'] = ''
		value = database_enabled()
		database_enabled.cache_clear()
		self.assertFalse(value)

	def test_database_connection_string(self):
		environ['DATABASE_CONNECTION_STRING'] \
			= 'postgres://admin:quest@127.0.0.1:8812'
		value = database_connection_string()
		database_connection_string.cache_clear()
		self.assertEqual('postgres://admin:quest@127.0.0.1:8812', value)

if __name__ == '__main__':
	main()