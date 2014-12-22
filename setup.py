from setuptools import setup

setup(name='replayer',
      version='0.1',
      description='Replay easily Apache access.logs',
      url='https://github.com/buechele/replayer',
      author='Andreas Buechele',
      author_email='andreas@buechele.org',
      license='MIT',
      packages=['replayer'],
      scripts=['bin/replayer'],
      install_requires=[
            'apachelog',
      ],
      zip_safe=False)
