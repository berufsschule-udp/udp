from os import environ
from unittest import TestCase, main
from gateway.frames_queue import FramesQueue

class TestReceiver(TestCase):
	frames_queue: FramesQueue

	def setUp(self):
		environ['MULTICAST'] = '239.0.43.36:4336'
		environ['NICS'] = '192.168.55.55'
		self.frames_queue = FramesQueue()
		self.frames_queue.init()

	def test_is_empty_when_empty(self):
		self.assertTrue(self.frames_queue.is_empty())

	def test_is_empty_when_not_empty(self):
		self.frames_queue.enqueue()
		self.assertFalse(self.frames_queue.is_empty())

	def test_dequeue_when_empty(self):
		self.assertRaises(IndexError, lambda: self.frames_queue.dequeue())

	def test_dequeue_when_not_empty(self):
		self.frames_queue.enqueue()
		self.assertIsNotNone(self.frames_queue.dequeue())

	def test_enqueue(self):
		self.assertRaises(IndexError, lambda: self.frames_queue.dequeue())
		self.frames_queue.enqueue()
		self.assertIsNotNone(self.frames_queue.dequeue())

if __name__ == '__main__':
	main()