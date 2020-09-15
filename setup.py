#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test as TestCommand

    class PyTest(TestCommand):
        def finalize_options(self):
            TestCommand.finalize_options(self)
            self.test_args = []
            self.test_suite = True  # pylint: disable=attribute-defined-outside-init

        def run_tests(self):
            import pytest

            errno = pytest.main(self.test_args)
            sys.exit(errno)


except ImportError:
    from distutils.core import setup

    PyTest = lambda x: x

try:
    long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
except OSError:
    long_description = None

setup(
    name="asyncactor",
    use_scm_version={"version_scheme": "guess-next-dev", "local_scheme": "dirty-tag"},
    setup_requires=["setuptools_scm"],
    description="Async decentralized actor",
    long_description=long_description,
    url="https://github.com/smurfix/asyncactor",
    author="Matthias Urlichs",
    author_email="matthias@urlichs.de",
    maintainer="Matthias Urlichs",
    maintainer_email="matthias@urlichs.de",
    keywords=["Serf", "MQTT", "orchestration", "service discovery", "anyio"],
    license="GPL3",
    packages=find_packages(),
    install_requires=["msgpack >= 0.5.0", "anyio >= 1.4", "outcome", "attrs >= 18.1"],
    extras_require={":python_version < '3.7'": ["async_generator", "async_exit_stack"]},
    tests_require=["pytest >= 2.5.2", "pytest-cov >= 2.3", "trio >= 0.15", "distmqtt >= 0.32"],
    cmdclass={"test": PyTest},
    python_requires=">=3.6",
)
