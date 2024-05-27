def start_version():
	from gateway.version import Version

	version = Version()
	version.init()
	print(version.VERSION)