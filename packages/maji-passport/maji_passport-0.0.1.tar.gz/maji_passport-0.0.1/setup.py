from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='maji_passport',
  version='0.0.1',
  author='ViktorTeodorih',
  author_email='viktorteodorihivanov@gmail.com',
  description='Maji Passport With custom authorisation',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://passport.maji.la/',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='maji passport python',
  project_urls={
    'Documentation': 'link'
  },
  python_requires='>=3.9'
)