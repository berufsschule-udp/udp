from typing import TYPE_CHECKING
from gateway.env import log_sql
from gateway.logger import trace

if TYPE_CHECKING:
	from asyncpg.pool import Pool

class Database:
	pool: 'Pool'

	async def init(self):
		from asyncpg import create_pool
		from gateway.logger import info
		from gateway.env import database_connection_string

		self.pool = await create_pool(dsn=database_connection_string())
		info(lambda: connection_info())

	async def execute(self, query: str, *params):
		async with self.pool.acquire() as connection:
			await connection.execute(query, *params)
			if log_sql(): trace(lambda: f'{params} {query}.')

def connection_info():
	from threading import current_thread
	return f'Connected to database from the thread {current_thread().name}.'