def parse_args():
	from argparse import ArgumentParser
	parser = ArgumentParser('gateway')

	parser.add_argument(
		'-v', '--version',
		action='store_true',
		help='show version'
	)

	parser.add_argument(
		'-b', '--build',
		nargs='?',
		const='build',
		help='build project'
	)

	return parser.parse_args()