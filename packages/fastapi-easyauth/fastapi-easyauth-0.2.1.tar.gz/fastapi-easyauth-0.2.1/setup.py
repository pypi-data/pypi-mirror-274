from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='fastapi-easyauth',
  version='0.2.1',
  author='duckduck',
  author_email='dimondtp@gmail.com',
  description='A library for quickly creating authentication using JWT and Cookies. Or storing a JWT token in a session',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Trejgus/fastapi-easyauth',
  packages=find_packages(),
  install_requires=[
      'fastapi',
      'fastapi-jwt',
      'pydantic',
      'itsdangerous'
      ],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='fastapi fastapi-jwt fastapi-easyauth fastapi-auth sessioauth SessioAuth',
  project_urls={
    'GitHub': 'https://github.com/Trejgus/fastapi-easyauth'
  },
  python_requires='>=3.6'
)