from setuptools import setup

setup(name='replayreqs',
      version='0.1',
      description='Replays Apache access logs',
      url='http://github.com/buechele/...',
      author='Andreas Buechele',
      author_email='andreas@buechele.org',
      license='MIT',
      packages=['replayreqs'],
      scripts=['bin/replayreqs'],
      install_requires=[
            'apachelog',
      ],
      zip_safe=False)