from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: End Users/Desktop',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='movieFinderIMDB',
  version='0.0.5',
  description='A moviefinder based on IMDB rating',
  long_description=open('README.md', encoding="utf-8").read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='https://github.com/NicolaiThomassen/moviefinder',  
  author='Nicolai Thomassen',
  author_email='Thomassen.nicolai@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['movie', 'imdb'],
  packages=find_packages(),
  install_requires=['IMDbPY==2021.4.18', 'pandas==1.3.1', 'requests==2.25.1'],
#  setup_requires=['IMDbPY==2021.4.18', 'pandas==1.3.1']
)
