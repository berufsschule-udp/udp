from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from gateway.logger import error

if TYPE_CHECKING:
	from gateway.database import Database
	from gateway.headers import AlarmLevel

@dataclass
class Alarm:
	role: str
	index: int
	"""Defaults for above and below are None,
	to add the current state on program init."""
	above: int = field(init=False, default=None)
	below: int = field(init=False, default=None)

	async def handle(self, level: 'AlarmLevel', database: 'Database'):
		if level.above == self.above and level.below == self.below:
			return

		try:
			await database.execute(
				'INSERT INTO events (channel_id, alarm_level, timestamp) ' +
				'VALUES ($1, $2, NOW())',
				f'{self.role}-{self.index}',
				max(level.above, level.below)
			)
		except Exception as exception:
			error(
				lambda: f'[{self.role}-{self.index}] Failed to ' +
				f'add event to database: {exception}'
			)

		self.above, self.below = level.above, level.below