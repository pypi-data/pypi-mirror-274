from setuptools import setup, find_packages
from pathlib import Path
import subprocess

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

def get_version_from_git():
    try:
        # Get the latest tag from Git
        version = subprocess.check_output(['git', 'describe', '--tags']).strip().decode('utf-8')
        # Ensure the version is in the correct format
        if version.startswith('v'):
            version = version[1:]
        return version
    except subprocess.CalledProcessError:
        # Handle the case where there are no tags or git is not available
        return "0.0.0"

setup(
    name='aprendo',
    version=get_version_from_git(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Quieres aprender español? "Aprendo" es la solución! Add, edit, conjugate, learn and test your Spanish verbs and vocab.',
    author='Lui Holliday',
    author_email='tech.luiholl@gmail.com',
    url='https://github.com/luiHoll97/aprendo',
    packages=find_packages(),
    install_requires=['questionary'],
)