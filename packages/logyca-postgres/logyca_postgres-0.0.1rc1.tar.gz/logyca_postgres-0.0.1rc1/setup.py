#!/usr/bin/env python
from setuptools import setup, find_packages

COMPANY_NAME="LOGYCA"
PACKAGE_NAME = "logyca-postgres"
VERSION = "0.0.1rc1"

install_requires = ["SQLAlchemy>=2.0.6","starlette>=0.24.0"]
install_requires_asyncpg = ["asyncpg >=0.27.0"]
install_requires_psycopg2 = ["psycopg2 >=2.9.6"]
install_requires_psycopg2_binary = ["psycopg2-binary >=2.9.6"]

extras_require = {
    "async": install_requires + install_requires_asyncpg,
    "sync-psycopg2": install_requires + install_requires_psycopg2,
    "sync-psycopg2-binary": install_requires + install_requires_psycopg2_binary,
    "async-sync-psycopg2": install_requires + install_requires_asyncpg + install_requires_psycopg2,
    "async-sync-psycopg2-binary": install_requires + install_requires_asyncpg + install_requires_psycopg2_binary,
}

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=f'An integration package created by the company {COMPANY_NAME} that connects Postgres and is used to standardize connections and dependency injection in synchronous or asynchronous mode. Tested in fastapi and in console/worker scripts.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Jaime Andres Cardona Carrillo',
    author_email='tecnologiaeinformacion@logyca.com',
    url='https://github.com/logyca/<soon>',
    keywords="postgres, driver database",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
)
