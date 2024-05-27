from bisect import bisect_right
from dataclasses import dataclass, field
from math import isnan
from time import time, time_ns
from typing import Optional, TYPE_CHECKING

from gateway.env import timestamp_check
from gateway.logger import error, info, warn

if TYPE_CHECKING:
	from gateway.database import Database
	from gateway.intervals import Intervals

@dataclass
class Calculator:
	role: str
	index: int
	intervals: 'Intervals'
	size: int
	values: list[tuple[float, int]] = field(init=False, default_factory=list)

	def push(self, value: float, timestamp: float):
		if len(self.values) == self.size:
			self.values.pop(0)

		filtered_timestamp = timestamp if timestamp_check() else int(time())
		self.values.append((value, filtered_timestamp))

	async def update_intervals(self, database: Optional['Database']):
		if not self.values:
			info(lambda: f'[{self.role}-{self.index}] No values received.')
			return

		timestamp = time_ns() // 1000
		intervals_values = self.intervals_values()

		if not intervals_values[0]:
			warn(
				lambda: f'[{self.role}-{self.index}] All received values ' +
				'are expired. Possibly wrong time settings.'
			)
			return

		for i in range(self.intervals.count()):
			self.intervals.push(average(intervals_values[i]), i)

		if not database:
			return

		value = self.intervals.values[0][-1]

		try:
			await database.execute(
				'INSERT INTO averages (channel_id, value, timestamp) ' +
				f'VALUES ($1, $2, {timestamp})',
				f'{self.role}-{self.index}',
				None if isnan(value) else value
			)
		except Exception as exception:
			error(
				lambda: f'[{self.role}-{self.index}] Failed to ' +
				f'add averages to database: {exception}'
			)

	def intervals_values(self):
		timestamp = int(time())
		values_and_seconds = [(v, timestamp - t) for v, t in self.values]
		intervals_values: list[list[float]] \
			= [[] for _ in range(self.intervals.count())]

		for value, seconds in reversed(values_and_seconds):
			# Inform if value is from the future.
			if seconds < 0:
				warn(
					lambda: f'[{self.role}-{self.index}] Received value ' +
					'is from future. Possibly wrong time settings.'
				)
				continue

			# Add value to the first interval.
			if (index := bisect_right(self.intervals.durations, seconds)) == 0:
				intervals_values[0].append(value)
				continue

			# Stop at the first expired value.
			if index == self.intervals.count():
				break

			# Take values from the previous interval.
			intervals_values[index] = self.intervals.values[index - 1][:]

		return intervals_values

def average(values: list[float]):
	if not values:
		return 0

	multiplier = 1
	for value in values: multiplier *= value
	return multiplier ** (1 / len(values))