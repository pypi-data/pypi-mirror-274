from setuptools import setup, find_packages

setup(
	name = 'pycamia',
	version = '1.0.40',
	keywords = ['pip', 'pymyc', 'pycamia', 'environment', 'path', 'touch'],
	description = 'The main package and a background support of project PyCAMIA. ',
	long_description = None,
	long_description_content_type = 'text/markdown',
	license = 'MIT Licence',
	url = 'https://github.com/Bertie97/PyZMyc/pycamia',
	author = 'Yuncheng Zhou',
	author_email = 'bertiezhou@163.com',
	packages = find_packages(),
	include_package_data = False,
	platforms = 'any',
	install_requires = ['tqdm']
)
