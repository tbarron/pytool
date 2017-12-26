from setuptools import setup
from pytool import version

setup(name="pytool",
      version=version._v,
      author="Tom Barron",
      author_email="tusculum@gmail.com",
      entry_points={'console_scripts': ["pytool = pytool:main"]}
      )
