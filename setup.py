from setuptools import setup

import replayer


setup(name='replayer',
      version=replayer.__version__,
      description='Replay easily an Apache access.log',
      url='https://github.com/buechele/replayer',
      author='Andreas Buechele',
      author_email='andreas@buechele.org',
      license='MIT',
      packages=['replayer'],
      scripts=['bin/replayer'],
      install_requires=[
          'apachelog',
          'requests>=2.6.0',
          'hurry.filesize',
      ],
      platforms='any',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Systems Administration'
      ],
      zip_safe=False)