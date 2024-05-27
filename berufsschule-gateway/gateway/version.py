PATH = 'VERSION'

class Version:
	COMPANY: str
	DESCRIPTION: str
	COPYRIGHT: str
	TRADEMARK_1: str
	TRADEMARK_2: str
	DOMAIN: str
	MAJOR: int
	MINOR: int
	PATCH: int
	BUILD: int
	STAGE: str
	VERSION_PATTERN: str
	VERSION: str

	def init(self):
		with open(PATH) as file:
			self.update(file.read().splitlines())

	def increment(self, build_type: str):
		if build_type == 'major':
			self.MAJOR += 1
			self.MINOR = self.PATCH = self.BUILD = 0
		elif build_type == 'minor':
			self.MINOR += 1
			self.PATCH = self.BUILD = 0
		elif build_type == 'patch':
			self.PATCH += 1
			self.BUILD = 0
		else:
			self.BUILD += 1

		self.VERSION = self.format_version()
		self.write_file()

	def update(self, lines: list[str]):
		for line in [l.strip() for l in lines if not l.isspace()]:
			if line.startswith('COMPANY'):
				self.COMPANY = line.replace('COMPANY', '').strip()
			elif line.startswith('DESCRIPTION'):
				self.DESCRIPTION = line.replace('DESCRIPTION', '').strip()
			elif line.startswith('COPYRIGHT'):
				self.COPYRIGHT = line.replace('COPYRIGHT', '').strip()
			elif line.startswith('TRADEMARK 1'):
				self.TRADEMARK_1 = line.replace('TRADEMARK 1', '').strip()
			elif line.startswith('TRADEMARK 2'):
				self.TRADEMARK_2 = line.replace('TRADEMARK 2', '').strip()
			elif line.startswith('DOMAIN'):
				self.DOMAIN = line.replace('DOMAIN', '').strip()
			elif line.startswith('MAJOR'):
				self.MAJOR = int(line.replace('MAJOR', ''))
			elif line.startswith('MINOR'):
				self.MINOR = int(line.replace('MINOR', ''))
			elif line.startswith('PATCH'):
				self.PATCH = int(line.replace('PATCH', ''))
			elif line.startswith('BUILD'):
				self.BUILD = int(line.replace('BUILD', ''))
			elif line.startswith('STAGE'):
				self.STAGE = line.replace('STAGE', '').strip()
			elif line.startswith('VERSION PATTERN'):
				self.VERSION_PATTERN = line \
					.replace('VERSION PATTERN', '') \
					.strip()

		self.VERSION = self.format_version()

	def format_version(self):
		return self.VERSION_PATTERN \
			.replace('MAJOR', str(self.MAJOR)) \
			.replace('MINOR', str(self.MINOR)) \
			.replace('PATCH', str(self.PATCH)) \
			.replace('BUILD', str(self.BUILD)) \
			.replace('STAGE', self.STAGE) \
			.strip()

	def write_file(self):
		content = f'''COMPANY				{self.COMPANY}
DESCRIPTION			{self.DESCRIPTION}
COPYRIGHT			{self.COPYRIGHT}
TRADEMARK 1			{self.TRADEMARK_1}
TRADEMARK 2			{self.TRADEMARK_2}
DOMAIN				{self.DOMAIN}

MAJOR				{self.MAJOR}
MINOR				{self.MINOR}
PATCH				{self.PATCH}
BUILD				{self.BUILD}
STAGE				{self.STAGE}
VERSION PATTERN		{self.VERSION_PATTERN}

VERSION				{self.VERSION}'''

		with open(PATH, 'w', newline='\n') as file:
			file.write(content)