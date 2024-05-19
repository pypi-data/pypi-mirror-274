from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description = fh.read()
else:
  long_description = ''

setup(
    name="gridlooper",
    packages=["gridlooper"],
    install_requires=['### gridlooper.py', 'dill==0.3.7', 'tqdm', 'attrs>=22.2.0'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan", author_email="parachute.repo@gmail.com", description="A tool to run experiments based on defined grid and function with single iteration.", version="0.0.2"
)
        