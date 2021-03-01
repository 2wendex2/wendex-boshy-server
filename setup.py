#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'wendexboshyserver',
    version = '0.0-SNAPSHOT',
    description = 'Wendex Boshy Server',
    author = 'Wendex',
    author_email = '2wendex2@mail.com',
    url = 'https://github.com/2wendex2/wendex-boshy-server',
    license = 'BSD 2-clause license',
    packages = [
        'wbs'
    ],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Pylacewing',
        'License :: OSI Approved :: BSD 2-clause License',
        'Programming Language :: Python :: 2',
        'Topic :: Communications',
        'Topic :: Internet'
    ]
)