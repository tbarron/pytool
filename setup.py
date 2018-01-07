from setuptools import setup

def execfile(fname, gdict, ldict):
    exec(compile(open(fname, 'rb').read(), fname, 'exec'),
         gdict,
         ldict)

execfile("./pytool/version.py", globals(), locals())

setup(name="pytool",
      version=__version__,
      description="Create python projects and programs",
      author="Tom Barron",
      author_email="tusculum@gmail.com",
      install_requires=[
          'docopt_dispatch',
          'py',
      ],
      packages=['pytool'],
      entry_points={'console_scripts': ["pytool = pytool:main"]}
      )
