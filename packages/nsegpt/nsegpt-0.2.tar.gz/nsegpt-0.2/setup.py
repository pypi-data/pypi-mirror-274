from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='nsegpt',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    include_package_data=True,
    description='A package to fetch stock data from NSE India',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='NiftyBilla',
    author_email='kaushal.developer@yahoo.com',
    url='https://github.com/Kaushal-developer/NSEGPT',
    project_urls={
        'Bug Tracker': 'https://github.com/Kaushal-developer/NSEGPT/issues',
        'Source Code': 'https://github.com/Kaushal-developer/NSEGPT',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
