def main():
	try:
		from gateway.env import init_env
		init_env()

		from gateway.logger import init_logger
		init_logger()

		from gateway.args import parse_args
		args = parse_args()

		if args.version:
			from gateway.starters.version import start_version
			start_version()
		elif args.build:
			from gateway.starters.build import start_build
			start_build(args.build)
		else:
			from asyncio import run
			from gateway.starters.main import Main
			run(Main().start_main())
	except Exception:
		from traceback import format_exc
		from gateway.logger import fatal
		fatal(lambda: format_exc())
	except KeyboardInterrupt:
		exit(130)

if __name__ == '__main__':
	main()