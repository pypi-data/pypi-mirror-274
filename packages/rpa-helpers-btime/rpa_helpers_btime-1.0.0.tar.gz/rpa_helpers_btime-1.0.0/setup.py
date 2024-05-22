from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="rpa-helpers-btime",
    version="1.0.0",
    description="Esse pacote irá oferecer todas as funcionalidades para auxiliar na programação de rpa.",
    long_description=Path("README.md").read_text(),
    author="Geovanne Zanata",
    author_email="geovanne.zanata@btime.com.br",
    keywords=['log', 'loggers'],
    packages=find_packages(),
)