import subprocess
from setuptools import setup, find_packages

_PACKAGE_NAME = "ntdgotv_langtools"


subprocess.run(
    [
        "pipreqs",
        "ntdggotv_langtools",
        "--use-local",
        "--savepath",
        "requirements.txt",
    ]
)

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

with open("dev-requirements.txt") as f:
    dev_requires = f.read().strip().split("\n")


with open("README.md", "r") as f:
    description = f.read()

setup(
    name=_PACKAGE_NAME,
    version="0.2.1",
    description=description,
    long_description=description,
    long_description_content_type="text/markdown",
    author="ntdGoTV",
    author_email="ntdGoTV@gmail.com",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={"dev": dev_requires},
)
