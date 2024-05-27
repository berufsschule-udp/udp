 from unittest import main, TestCase
 from unittest.mock import mock_open, patch

 from gateway.version.version import Version

 class TestVersion(TestCase):
 	def test_version_initialize(self) -> None:
 		major_version = 4
 		minor_version = 6
 		patch_version = 19
 		build_version = 429
 		stage_version = 'ratio'

 		expected_version = \
 			f'{major_version}shrink{minor_version}.{patch_version}68{build_version}' \
 			f'{stage_version} COMPANY'

 		content = self.__get_content(
 			company='reason',
 			major_version=major_version,
 			minor_version=minor_version,
 			patch_version=patch_version,
 			build_version=build_version,
 			stage_version=stage_version,
 			version_pattern='MAJORshrinkMINOR.PATCH68BUILDSTAGE COMPANY'
 		)

 		with patch('builtins.open', mock_open(read_data=content)):
 			version = Version()
 			version.initialize()
 			self.assertEqual(version.version, expected_version)

 	def test_version_increment_build(self) -> None:
 		major_version = 2
 		minor_version = 9
 		patch_version = 44
 		build_version = 580

 		expected_version = f'{major_version}.{minor_version}.{patch_version}.{build_version + 1}'

 		content = self.__get_content(
 			major_version=major_version,
 			minor_version=minor_version,
 			patch_version=patch_version,
 			build_version=build_version,
 			version_pattern='MAJOR.MINOR.PATCH.BUILD'
 		)

 		with patch('builtins.open', mock_open(read_data=content)):
 			version = Version()
 			version.initialize()
 			version.increment('build')
 			self.assertEqual(version.version, expected_version)

 	def test_version_increment_patch(self) -> None:
 		major_version = 5
 		minor_version = 5
 		patch_version = 12

 		expected_version = f'{major_version}.{minor_version}.{patch_version + 1}.{0}'

 		content = self.__get_content(
 			major_version=major_version,
 			minor_version=minor_version,
 			patch_version=patch_version,
 			build_version=484,
 			version_pattern='MAJOR.MINOR.PATCH.BUILD'
 		)

 		with patch('builtins.open', mock_open(read_data=content)):
 			version = Version()
 			version.initialize()
 			version.increment('patch')
 			self.assertEqual(version.version, expected_version)

 	def test_version_increment_minor(self) -> None:
 		major_version = 2
 		minor_version = 6

 		expected_version = f'{major_version}.{minor_version + 1}.{0}.{0}'

 		content = self.__get_content(
 			major_version=major_version,
 			minor_version=minor_version,
 			patch_version=48,
 			build_version=964,
 			version_pattern='MAJOR.MINOR.PATCH.BUILD'
 		)

 		with patch('builtins.open', mock_open(read_data=content)):
 			version = Version()
 			version.initialize()
 			version.increment('minor')
 			self.assertEqual(version.version, expected_version)

 	def test_version_increment_major(self) -> None:
 		major_version = 1

 		expected_version = f'{major_version + 1}.{0}.{0}.{0}'

 		content = self.__get_content(
 			major_version=major_version,
 			minor_version=3,
 			patch_version=47,
 			build_version=675,
 			version_pattern='MAJOR.MINOR.PATCH.BUILD'
 		)

 		with patch('builtins.open', mock_open(read_data=content)):
 			version = Version()
 			version.initialize()
 			version.increment('major')
 			self.assertEqual(version.version, expected_version)

 	@staticmethod
 	def __get_content(
 			company: str = '_',
 			description: str = '_',
 			copyright_text: str = '_',
 			trademark_1: str = '_',
 			trademark_2: str = '_',
 			domain: str = '_',
 			major_version: int = 0,
 			minor_version: int = 0,
 			patch_version: int = 0,
 			build_version: int = 0,
 			stage_version: str = '_',
 			version_pattern: str = '_'
 	) -> str:
 		return \
 			f'COMPANY            {company}\n' \
 			f'DESCRIPTION        {description}\n' \
 			f'COPYRIGHT          {copyright_text}\n' \
 			f'TRADEMARK 1        {trademark_1}\n' \
 			f'TRADEMARK 2        {trademark_2}\n' \
 			f'DOMAIN             {domain}\n' \
 			'\n' \
 			f'MAJOR              {major_version}\n' \
 			f'MINOR              {minor_version}\n' \
 			f'PATCH              {patch_version}\n' \
 			f'BUILD              {build_version}\n' \
 			f'STAGE              {stage_version}\n' \
 			f'VERSION PATTERN    {version_pattern}'

 if __name__ == '__main__':
 	main()