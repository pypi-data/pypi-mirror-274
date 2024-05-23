import os
from setuptools import (
    find_namespace_packages,
    setup,
)

DESCRIPTION = 'Snowflake Native App Permission SDK Stub'
LONG_DESCRIPTION = 'This package provides a set of stub functions that replaces the permissions SDK for local testing'
SNOWFLAKE_PERMISSIONS_SRC_DIR = os.path.join("src", "snowflake")

def get_version():
    version = {}
    with open('src/snowflake/version.py') as fp:
        exec(fp.read(), version)
    return version['__version__']

setup(
    name="snowflake-native-apps-permission-stub",
    version=get_version(),
    author='Snowflake, Inc',
    author_email='support@snowflake.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[
        'setuptools >= 40.0.0',
    ],
    packages=find_namespace_packages(
        where='src'
    ),
    package_dir={
        '': 'src',
    },
    keywords='Snowflake db database cloud warehouse permissions sdk native apps',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: SQL",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=True,
)

