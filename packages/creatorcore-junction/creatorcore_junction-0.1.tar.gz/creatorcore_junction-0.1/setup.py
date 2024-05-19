from setuptools import setup

installation_requirements = [
    "requests==2.31.0"
]

test_requirements = [
    "pytest==8.2.0"
]

setup(
    name="creatorcore_junction",
    description="Handy python bindings for querying junction",
    version="0.1",
    author="(~)",
    package_dir={"": "packages"},
    packages=["creatorcore_junction"],
    install_requires=installation_requirements,
    tests_require=test_requirements,
)
