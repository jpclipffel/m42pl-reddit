from setuptools import setup


setup(
  name='m42pl-reddit',
  author='@jpclipffel',
  url='https://github.com/jpclipffel/m42pl-reddit',
  version='1.0.0',
  packages=['m42pl_reddit',],
  install_requires=[
    'm42pl',
    # ---
    'asyncpraw'
  ]
)
