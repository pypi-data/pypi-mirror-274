# setup.py
from setuptools import setup, find_packages

setup(
    name='hypercrawl',
    version='0.1.1',
    description='A simple asynchronous web crawler for scraping all URLs within a domain',
    author='Udit Akhouri',
    author_email='udit_2312res708@iitp.ac.in',
    url='https://github.com/uditakhourii/hypercrawl',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
        'nest_asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
) 
