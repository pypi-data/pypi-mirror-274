from setuptools import find_packages, setup

# define constants for working
NAME = 'EmLiLetter'
VERSION = '0.0.2'
DESCRIPTION = 'EmLi software to send mails for several users'
AUTHOR = 'Artem Tomilo'
REQUIRED = ['pygobject']
URL = 'https://gitlab.com/bridgearchitect/emli'
LICENSE = 'MIT'
PACKAGES = ['emli']
PACKAGE_DATA = 'emli.glade'

# start setupping process for PyPi repository
setup(
   name=NAME,
   version=VERSION,
   description=DESCRIPTION,
   author=AUTHOR,
   url=URL,
   license=LICENSE,
   packages=PACKAGES,
   install_requires=REQUIRED,
   package_data={'emli': [PACKAGE_DATA]},
   entry_points = {
   'console_scripts': ['emli=emli.emli:main'],
   },
)
