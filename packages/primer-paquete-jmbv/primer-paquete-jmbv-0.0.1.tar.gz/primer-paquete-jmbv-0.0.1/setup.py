from setuptools import setup, find_packages
from os import path

wworking_directory = path.abspath(path.dirname(__file__))

with open(path.join(wworking_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="primer-paquete-jmbv",
    version="0.0.1",
    description="El primer paqquete de Python que he creado",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juanmabv/primer_paquete",
    author="Juan Manuel Batista Velásquez",
    author_email="juanmabatistav@gmail.com",
    packages=find_packages(),
    install_requires=[],
)
