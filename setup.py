#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='mediasync',
      version='0.1',
      description='Python utility for smart syncing media files',
      author='Eli Segal',
      author_email='eli.segal@gmail.com',
      url='https://github.com/rockem/MediaSync',
      install_requires=['setuptools', 'click', 'mutagen', 'behave'],
      packages=['mediasync'],
      entry_points="""
      [console_scripts]
      media-sync = mediasync.app:main
      """

)