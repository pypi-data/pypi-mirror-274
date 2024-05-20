from setuptools import setup, find_packages
from pathlib import Path
import subprocess

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name='aprendo',
    version="0.0.1",
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Quieres aprender español? "Aprendo" es la solución! Add, edit, conjugate, learn and test your Spanish verbs and vocab.',
    author='Lui Holliday',
    author_email='tech.luiholl@gmail.com',
    url='https://github.com/luiHoll97/aprendo',
    packages=find_packages(),
    install_requires=['questionary'],
)
