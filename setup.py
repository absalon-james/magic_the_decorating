from setuptools import setup

setup(
    name="magic_the_decorating",
    version="0.0.0",
    author="james absalon",
    author_email="james.absalon@rackspace.com",
    packages=['magic_the_decorating'],
    package_data={'magic_the_decorating': ['magic_the_decorating/*']},
    long_description="Tool for decorating modules on import."
)
