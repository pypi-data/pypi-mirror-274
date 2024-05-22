from setuptools import setup, find_packages
from pathlib import Path

# try:
#     long_description = Path("README.md").read_text()
# except FileNotFoundError:
#     long_description = "Default long description if README.md is not found."

setup(
    name="rpa-helpers-btime",
    version="1.0.1",
    description="Esse pacote irá oferecer todas as funcionalidades para auxiliar na programação de rpa.",
    long_description="Default long description if README.md is not found.",
    author="Geovanne Zanata",
    author_email="geovanne.zanata@btime.com.br",
    keywords=['log', 'loggers'],
    packages=find_packages(),
)