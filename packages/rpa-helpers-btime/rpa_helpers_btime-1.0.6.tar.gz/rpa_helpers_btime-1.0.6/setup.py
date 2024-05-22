from setuptools import setup, find_packages
from pathlib import Path

# try:
#     long_description = Path("README.md").read_text()
# except FileNotFoundError:
#     long_description = "Default long description if README.md is not found."

setup(
    name="rpa-helpers-btime",
    version="1.0.6",
    description="Esse pacote irá oferecer todas as funcionalidades para auxiliar na programação de rpa.",
    long_description="Default long description if README.md is not found.",
    author="Geovanne Zanata",
    author_email="geovanne.zanata@btime.com.br",
    keywords=['log', 'loggers'],
    packages=find_packages(),
    install_requires=[
                'colorama==0.4.6',
                'flake8==7.0.0',
                'greenlet==3.0.3',
                'loguru==0.7.2',
                'mccabe==0.7.0',
                'setuptools==69.5.1',
                'pycodestyle==2.11.1',
                'pyflakes==3.2.0',
                'SQLAlchemy==2.0.30',
                'typing_extensions==4.11.0',
                'win32-setctime==1.1.0',
            ],
)