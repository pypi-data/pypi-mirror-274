"""mstache setuptools script."""
"""
mstache, Mustache for Python
============================

See `README.md` provided as part of source distributions or available online
at the `project repository`_.

.. _README.md: https://gitlab.com/ergoithz/mstache/-/blob/master/README.md
.. _project repository: https://gitlab.com/ergoithz/mstache


License
-------

Copyright (c) 2021-2024, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/mstache/-/blob/master/LICENSE

"""

import os
import pathlib
import re
import time

from setuptools import setup

repository = 'https://gitlab.com/ergoithz/mstache'

readme_source, module_source = (
    pathlib.Path(name).read_text(encoding='utf8')
    for name in ('README.md', 'mstache.py')
    )
readme = re.sub(
    r'(?P<prefix>!?)\[(?P<text>[^]]+)\]\(\./(?P<src>[^)]+)\)',
    lambda match: (
        '{prefix}[{text}]({repository}/-/{view}/master/{src})'.format(
            repository=repository,
            view='raw' if match.group('prefix') == '!' else 'blob',
            **match.groupdict(),
            )),
    readme_source,
    )
metadata = dict(m.groups() for m in re.finditer(
    r"__(author|email|license|version)__ = '([^']+)'",
    module_source,
    ))
version = (
    metadata['version'] if os.getenv('TWINE_REPOSITORY') == 'pypi' else
    '{}a{}{:02d}{:02d}'.format(metadata['version'], *time.gmtime()[:3])
    )
extras_require = {
    'codestyle': [
        'pycodestyle',
        'ruff',
        'sphinx',
        'rstcheck',
        'mypy',
        ],
    'coverage': [
        'coverage[toml]',
        ],
    'docs': [
        'recommonmark',
        'sphinx',
        'sphinx-autobuild',
        'sphinx-autodoc-typehints',
        ],
    'release': [
        'build',
        'twine',
        ],
    'benchmark': [
        'ustache==0.1.5',
        'chevron',
        'tabulate',
        ],
    'dev': [],
    }
setup(
    name='mstache',
    version=version,
    url=repository,
    license=metadata['license'],
    author=metadata['author'],
    author_email=metadata['email'],
    description='mstache, Mustache for Python',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        ],
    python_requires='>=3.10.0',
    extras_require={
        **extras_require,
        'dev': [
            extra
            for extra_group in extras_require.values()
            for extra in extra_group
            ],
        },
    keywords=['template', 'mustache'],
    py_modules=['mstache'],
    entry_points={
        'console_scripts': (
            'ustache=mstache:cli',
            'mstache=mstache:cli',
            ),
        },
    test_suite='tests',
    platforms='any',
    zip_safe=True,
    )
