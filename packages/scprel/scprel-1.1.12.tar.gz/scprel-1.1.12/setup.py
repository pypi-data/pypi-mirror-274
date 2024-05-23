from setuptools import setup, find_packages
import os
#import codecs

VERSION = '1.1.12'
DESCRIPTION = 'Single-cell data preprocessing for multiple samples.'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
 #   long_description = "\n" + fh.read()

# Setting up
setup(
    name="scprel",
    version=VERSION,
    author="GPuzanov (Grigory Puzanov)",
    author_email="<grigorypuzanov@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    readme="README.md",
    packages=find_packages(include=['scprel']),
    url='https://pypi.org/project/scprel/',
    license_files = ('LICENSE.txt',),
    install_requires=['omnipath', 'infercnvpy', 'anndata', 'decoupler', 'hdf5plugin', 'scanpy', 'scrublet', 'adjustText', 'wget'],
    keywords=['python', 'jupyter notebook', 'single-cell', 'scRNA-seq', 'single-cell quality control', 'single-cell data preparation', 'single-cell multiple samples', 'samples concatenation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)