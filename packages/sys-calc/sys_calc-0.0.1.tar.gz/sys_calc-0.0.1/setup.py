from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='sys_calc',
  version='0.0.1',
  author='S4CBS',
  author_email='aap200789@gmail.com',
  description='This is the simplest module for quick work with float - bin,oct,hex.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/S4CBS/sys_calc',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='sys_calc ',
  project_urls={
    'GitHub': 'https://github.com/S4CBS/sys_calc'
  },
  python_requires='>=3.6'
)