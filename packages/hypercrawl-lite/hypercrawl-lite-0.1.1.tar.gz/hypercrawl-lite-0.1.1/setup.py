from setuptools import setup, find_packages

setup(
    name='hypercrawl-lite',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'hypercrawl-lite=hypercrawl_lite.scraper:main'
        ]
    },
    author='Udit Akhouri',
    description='A lightweight web scraper for extracting URLs from a webpage. This is utlrafastlite version of Hypercrawl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/hypercrawl-lite',
)

