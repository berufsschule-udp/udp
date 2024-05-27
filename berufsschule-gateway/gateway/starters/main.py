from asyncio import run
from math import nan
from threading import Thread
from time import sleep, time

from gateway.alarm import Alarm
from gateway.calculator import Calculator
from gateway.database import Database
from gateway.env import channel_max_frames_per_second, channels_role_and_indexes, database_enabled
from gateway.frames_queue import FramesQueue
from gateway.headers import VmpEvent
from gateway.intervals import Intervals

class Main:
	frames_queue: FramesQueue
	intervals: Intervals
	calculators: list[Calculator]

	def __init__(self):
		self.frames_queue = FramesQueue()
		self.intervals = Intervals()

	async def start_main(self):
		self.frames_queue.init()
		self.intervals.init()

		calculators_count = channel_max_frames_per_second() \
		    * self.intervals.durations[-1]

		self.calculators = [
			Calculator(r, v, self.intervals, calculators_count)
			for r, v in channels_role_and_indexes()
		]

		Thread(target=self.start_receive_frames, name='ReceiveFramesThread') \
			.start()

		Thread(target=self.start_handle_frames, name='HandleFramesThread') \
			.start()

		await self.start_average_intervals()

	def start_receive_frames(self):
		while True:
			self.frames_queue.enqueue()

	def start_handle_frames(self):
		run(self.start_handle_frames_async())

	async def start_handle_frames_async(self):
		alarms = [Alarm(r, i) for r, i in channels_role_and_indexes()]

		if database_enabled():
			database = Database()
			await database.init()
		else:
			database = None

		while True:
			if self.frames_queue.is_empty():
				continue

			try:
				vmp_event = VmpEvent \
					.from_buffer_copy(self.frames_queue.dequeue())
			except ValueError:
				continue

			if not vmp_event.event:
				continue

			for calculator in self.calculators:
				if calculator.role != vmp_event.header.role:
					continue

				work_mode = vmp_event.events.work_mode
				value = vmp_event.values[calculator.index] if work_mode else nan
				calculator.push(value, vmp_event.ptp.seconds)

			if not database:
				continue

			for alarm in [a for a in alarms if a.role == vmp_event.header.role]:
				alarm_level = vmp_event.events.alarm_levels[alarm.index]
				await alarm.handle(alarm_level, database)

	async def start_average_intervals(self):
		if database_enabled():
			database = Database()
			await database.init()
		else:
			database = None

		update_time = time()

		while True:
			update_time += self.intervals.durations[0]
			sleep(max(update_time - time(), 0))

			for calculator in self.calculators:
				await calculator.update_intervals(database)