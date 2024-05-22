from setuptools import setup, find_packages

setup(
	name = 'batorch',
	version = '1.0.54',
	keywords = ['pip', 'pymyc', 'batorch', 'torch', 'batch', 'batched data'],
	description = "'batorch' is an extension of package torch, for tensors with batch dimensions. ",
	long_description = None,
	long_description_content_type = 'text/markdown',
	license = 'MIT Licence',
	url = 'https://github.com/Bertie97/PyZMyc/batorch',
	author = 'Yuncheng Zhou',
	author_email = 'bertiezhou@163.com',
	packages = find_packages(),
	include_package_data = False,
	platforms = 'any',
	install_requires = ['pycamia', 'torch', 'pynvml', 'matplotlib', 'psutil', 'numpy', 'pyoverload', 'sympy']
)
