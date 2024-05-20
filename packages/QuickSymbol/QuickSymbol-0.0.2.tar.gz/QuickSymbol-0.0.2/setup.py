from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='QuickSymbol',
  version='0.0.2',
  description='A symbol library for simple use',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ibrahim Abushawish',
  author_email='ibrahim.hamed2701@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='symbol', 
  packages=find_packages(),
  install_requires=[''] 
)