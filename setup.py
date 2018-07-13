import io
import os
from typing import Dict, Text, List

from setuptools import find_packages, setup


NAME = 'baseball_utils'
DESCRIPTION = 'A collection of baseball related utilities'
URL = 'https://github.com/mvwicky/baseball-utils'
EMAIL = 'mvanwickle@gmail.com'
AUTHOR = 'Michael Van Wickle'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None

REQUIRED = [
    'attrs>=18.1.0',
    'click',
    'colorama',
    'lxml',
    'requests_html',
    'mypy',
    'mypy_extensions',
    'flask',
    'flask-compress',
]

EXTRAS: Dict[Text, List[Text]] = {}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about: Dict[Text, Text] = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={'console_scripts': ['bbcli=baseball_utils.cli:cli']},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
