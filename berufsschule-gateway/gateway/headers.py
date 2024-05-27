from ctypes import Structure, Union, c_bool, c_char, c_float, c_int32, \
	c_uint32, c_uint8
from functools import cached_property

ALIVE = 'A'
EVENT = 'E'

class VmpHeader(Structure):
	name: str
	variant: str
	device_id: int
	channel_id: int
	role: str
	_name: bytes
	_variant: bytes
	_role: bytes
	_pack_ = 1
	_fields_ = [
		('_name', c_char * 4),
		('_variant', c_char),
		('device_id', c_uint32),
		('channel_id', c_uint8),
		('_role', c_char * 5)
	]

	@cached_property
	def name(self):
		return self._name.decode()

	@cached_property
	def variant(self):
		return self._variant.decode()

	@cached_property
	def role(self):
		return self._role.decode()

class Ptp(Structure):
	seconds: int
	nanos: int
	_pack_ = 1
	_fields_ = [
		('seconds', c_int32),
		('nanos', c_int32)
	]

class AlarmLevelInternal(Structure):
	above: int
	below: int
	leap: bool
	trend: bool
	_pack_ = 1
	_fields_ = [
		('above', c_uint8, 2),
		('below', c_uint8, 2),
		('leap', c_bool, 1),
		('trend', c_bool, 1)
	]

class AlarmLevel(Union):
	status: int
	_level: AlarmLevelInternal
	_fields_ = [
		('_level', AlarmLevelInternal),
		('status', c_uint8)
	]

	@property
	def above(self):
		return self._level.above

	@property
	def below(self):
		return self._level.below

	@property
	def leap(self):
		return self._level.leap

	@property
	def trend(self):
		return self._level.trend

class VmpEvents(Structure):
	sensor_status: int
	sensor_error: bool
	fault: bool
	alarm_levels: list[AlarmLevel]
	trend: bool
	rotation_mode: int
	not_master: bool
	work_mode: bool
	_alarm_levels: 'c_float_Array'
	_pack_ = 1
	_fields_ = [
		('sensor_status', c_uint8, 3),
		('sensor_error', c_bool, 1),
		('fault', c_bool, 1),
		('_alarm_levels', AlarmLevel * 6),
		('trend', c_bool, 1),
		('rotation_mode', c_uint8, 3),
		('not_master', c_bool, 1),
		('work_mode', c_bool, 1)
	]

	@cached_property
	def alarm_levels(self):
		return list(self._alarm_levels)

class VmpEvent(Structure):
	from gateway.env import channel_values_count

	header: VmpHeader
	ptp: Ptp
	values: list[float]
	events: VmpEvents
	_values: 'c_float_Array'
	_pack_ = 1
	_fields_ = [
		('header', VmpHeader),
		('ptp', Ptp),
		('_values', c_float * channel_values_count()),
		('events', VmpEvents)
	]

	@property
	def values(self):
		return list(self._values)

	@property
	def event(self):
		return self.header.variant == EVENT