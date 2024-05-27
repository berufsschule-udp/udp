from socket import AF_INET, IPPROTO_IP, IPPROTO_UDP, IP_ADD_MEMBERSHIP, \
	IP_MULTICAST_LOOP, IP_MULTICAST_TTL, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, \
	inet_aton, socket

from gateway.env import log_frames, multicast_ip_and_port, nics
from gateway.logger import trace

class FramesQueue:
	ip: str
	port: int
	queue: list[bytes]
	sock: socket

	def __init__(self):
		self.ip, self.port = multicast_ip_and_port()
		self.queue = []

	def init(self):
		self.sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 1)
		self.sock.setsockopt(IPPROTO_IP, IP_MULTICAST_LOOP, 1)
		self.sock.bind(('', self.port))
		request = inet_aton(self.ip) + b''.join(inet_aton(n) for n in nics())
		self.sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, request)

	def is_empty(self):
		return not self.queue

	def enqueue(self):
		frame = self.sock.recv(512)
		self.queue.append(frame)

		if log_frames():
			trace(lambda: f'[{self.ip}:{self.port}] {frame}.')

	def dequeue(self):
		return self.queue.pop(0)