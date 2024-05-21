"""Setup file for the Hermes package."""

from setuptools import find_packages, setup

setup(
    name="hermes-cai",
    version="0.0.2",
    packages=find_packages(include=["src", "src.*"]),
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
