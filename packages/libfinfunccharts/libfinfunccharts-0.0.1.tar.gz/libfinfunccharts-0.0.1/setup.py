from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()


setup(
  name='libfinfunccharts',
  version='0.0.1',
  author='qu1cky',
  author_email='qu1ck3r526@gmail.com',
  description='This library is a set of functions for financial calculations and the construction of charts and graphs.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='library finance charts ',
  project_urls={
    'GitHub': 'https://github.com/qu1cky25/libfinfunc'
  },
  python_requires='>=3.7'
)