# from pkg_resources import parse_requirements
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="blackboxai",
    version="2.8",
    packages=find_packages(),
    package_dir = {'': '.'},
    include_package_data=True,
    setup_requires= ['requests'],
    entry_points={
        "console_scripts": [
            "blackboxai = blackboxai:runChat"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)