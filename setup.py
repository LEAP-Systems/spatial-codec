# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# meta-data.
NAME = 'scodec'
DESCRIPTION = 'Spatial encoding algorithm using psuedo hilbert curves'
EMAIL = 'christian@leapsystems.online'
AUTHOR = 'cSDes1gn'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = False

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), 'r') as requirements:
    REQUIRED = list()
    for line in requirements.readlines():
        REQUIRED.append(line)

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url='https://leapsystems.online',
    download_url='https://github.com/Incuvers/iris-stage/archive/0.0.1.tar.gz',
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['wheel'],
    install_requires=REQUIRED,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
