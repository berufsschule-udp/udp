from gateway.env import intervals

class Intervals:
	durations: list[int]
	sizes: list[int]
	values: list[list[float]]

	def __init__(self):
		self.durations = []
		self.sizes = []
		self.values = []

	def init(self):
		durations = intervals()
		durations_count = len(durations)

		for i in range(durations_count):
			self.durations.append(durations[i])
			self.sizes.append(
				durations[i + 1] // durations[i]
				if i < durations_count - 1 else 1
			)
			self.values.append([])

	def push(self, value: float, index: int):
		if len(self.values[index]) == self.sizes[index]:
			self.values[index].pop(0)

		self.values[index].append(value)

	def count(self):
		return len(self.durations)