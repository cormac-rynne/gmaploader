from setuptools import setup, find_packages
import re
import os

# Get version from __init__.py
version_rgx = re.compile("""__version__[\s]*=[\s]*['|"](.*)['|"]""")
root_folder = os.path.dirname(__file__)
init_filepath = os.path.join(root_folder, 'gmaploader', '__init__.py')
with open(init_filepath, 'r') as f:
    text = f.read()
    match = version_rgx.search(text)
    version = match.group(1)

# Read README.md for long description
readme_filepath = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_filepath, 'r') as f:
    long_description = f.read()

SETUP_ARGS = dict(
    name='gmaploader',
    version=version,
    description='Google Map Static Image Loader',
    url='https://github.com/cormac-rynne/gmaploader.git',
    long_description=long_description,
    author='Cormac Rynne',
    author_email='cormac.ry@gmail.com',
    license='MIT',
    packages=find_packages(include=['gmaploader', 'gmaploader.*']),
    install_requires=[
        'matplotlib>=3.3.4',
        'Pillow>=9.0.0'
    ],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
)

if __name__ == '__main__':
    setup(**SETUP_ARGS)
