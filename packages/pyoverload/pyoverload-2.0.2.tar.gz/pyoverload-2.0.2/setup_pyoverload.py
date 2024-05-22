from setuptools import setup, find_packages

setup(
	name = 'pyoverload',
	version = '2.0.2',
	keywords = ['pip', 'pymyc', 'pyoverload', 'overload'],
	description = "'pyoverload' overloads the functions by simply using typehints and adding decorator '@overload'. ",
	long_description = None,
	long_description_content_type = 'text/markdown',
	license = 'MIT Licence',
	url = 'https://github.com/Bertie97/PyZMyc/pyoverload',
	author = 'Yuncheng Zhou',
	author_email = 'bertiezhou@163.com',
	packages = find_packages(),
	include_package_data = False,
	platforms = 'any',
	install_requires = ['pycamia']
)
