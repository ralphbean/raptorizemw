from setuptools import setup, find_packages
import sys, os

f = open('README.rst')
long_description = f.read()
f.close()

version = '0.2.0'

setup(name='raptorizemw',
      version=version,
      description="Every WSGI app is better with a raptor.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='raptor raptorize hilarity',
      author='Ralph Bean',
      author_email='ralph.bean@gmail.com',
      url='http://github.com/ralphbean/raptorizemw',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'webob',
          'weberror',
          'BeautifulSoup<4.0a1',
      ],
      entry_points="""
      [paste.filter_app_factory]
      middleware = raptorizemw:make_middleware
      main = raptorizemw:make_middleware
      """,
      )
