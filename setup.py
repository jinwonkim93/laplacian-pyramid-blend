from setuptools import setup, find_packages

setup(
  name = 'laplacian-pyramid-blend',
  packages = find_packages(exclude=[]),
  version = '0.0.1',
  license='MIT',
  description = 'laplacian-pyramid-blend',
  author = 'Jinwon Kim',
  author_email = 'code.eric22@gmail.com',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/jinwonkim93/laplacian-pyramid-blend',
  keywords = [
    'laplacian-pyramid-blend',
    'image'
  ],
  install_requires=[
    'opencv-python',
    'numpy',
  ],
)