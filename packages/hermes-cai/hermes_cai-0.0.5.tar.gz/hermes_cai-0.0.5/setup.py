"""Setup file for the Hermes package."""

from setuptools import find_packages, setup
import os

# Get the current directory of the setup.py script
here = os.path.abspath(os.path.dirname(__file__))

# Read the version from the VERSION file
with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name="hermes-cai",
    version=version,
    packages=find_packages(include=["hermes_cai", "hermes_cai.*"]),
    install_requires=[],
    author="James Groeneveld",
    author_email="james@character.ai",
    description="Defining and constructing production-grade prompts via an expressive templating engine.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/character-tech/chat-stack",
    python_requires=">=3.10",
    license="MIT",
)
