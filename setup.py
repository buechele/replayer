from setuptools import setup

setup(name='replayer',
      version='0.2.2',
      description='Replay easily an Apache access.log',
      url='https://github.com/buechele/replayer',
      author='Andreas Buechele',
      author_email='andreas@buechele.org',
      license='MIT',
      packages=['replayer'],
      scripts=['bin/replayer'],
      install_requires=[
          'apachelog',
      ],
      platforms='any',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Systems Administration'
      ],
      zip_safe=False)