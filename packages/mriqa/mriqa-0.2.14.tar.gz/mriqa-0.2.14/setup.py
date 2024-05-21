# -*- coding: utf-8 -*-
"""setup.py."""

from setuptools import setup

from os.path import join, dirname, abspath

# Single definition of __version__ in version.py
__version__ = 'UNDEFINED'
with open(join(dirname(__file__), 'mriqa', 'version.py')) as f:
    exec(f.read())

def readme(fname):
    path = abspath(join(dirname(__file__), fname))
    with open(path, encoding='utf-8') as f:
        return f.read()

config = {
    'name': 'mriqa',
    'description': 'Tools for MRI QA',
    'long_description': readme('README.md'),
    'long_description_content_type': 'text/markdown',
    'version': __version__,
    'author': 'Ronald Hartley-Davies',
    'author_email': 'R.Hartley-Davies@physics.org',
    'license': 'MIT',
    'url': 'https://bitbucket.org/rtrhd/mriqa.git',
    'download_url': 'https://bitbucket.org/rtrhd/mriqa/get/v%s.zip' % __version__,
    'tests_require': ['pytest'],
    'install_requires': [
        'numpy>=1.20.0',
        'scipy>=0.19.1',
        'matplotlib>=2.1.1',
        'pandas>=0.23.3',
        'xarray>=0.20.2',
        'scikit-image>0.14.0',
        'statsmodels>=0.12.2',
        'pydicom>=1.2.1',
        'dcmfetch>=0.3.1',
        'dcmextras>=0.3.4'
    ],
    'packages': ['mriqa', 'mriqa.xmlqa', 'mriqa.reports'],
    'package_data': {'mriqa': []},
    'scripts': [],
    'keywords': "mri qa phantom",
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
}

setup(**config)
