import setuptools
import pathlib

setuptools.setup(
name="gaurav",
version="0.1.0",
description="Brief description",
long_description=pathlib.Path("README.md").read_text(),
long_description_content_type="text/markdown",
url="https://abc.com",
author="Gaurav Mehta",
author_email="gewgawrav@gmail.com",
license="The Unlicense",
project_urls={
"Source": "https://github.com/gewgawrav/first-python-package",
},
python_requires="<3.12",
install_requires=['requests'],
packages=setuptools.find_packages(),
include_package_data=True,
entry_points={"console_scripts":["gaurav = gaurav.cli:main"]},


)