def start_build(build_type: str):
	from gateway.logger import info
	from gateway.version import Version

	info(lambda: f'Incrementing {build_type}...')
	version = Version()
	version.init()
	version.increment(build_type)
	info(lambda: f'Version: {version.VERSION}')