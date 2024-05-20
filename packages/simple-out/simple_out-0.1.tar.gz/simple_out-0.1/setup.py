from setuptools import setup

with open("README.md", "r") as read:
    long_description = read.read()

setup(
    name="simple-out",
    version="0.1",
    description="A simple way to print colored text in the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["print", "output", "input"],
    author="2Bor3d",
    packages=["out"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    url="https://github.com/2Bor3d/out"
)
