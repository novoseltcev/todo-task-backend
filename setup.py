from setuptools import setup, find_packages

NAME = 'server'
DESCRIPTION = ''

setup(
    name=NAME,
    version=__import__(NAME).__version__,
    description=DESCRIPTION,
    author='Novoseltcev Stanislav',
    namespace_packages=['server', 'crud', 'handler'],
    packages=find_packages(),
    platforms='Linux',
    zip_safe=False,
    include_package_data=True,
)
