# This file needs to be run with arguments as
# python3 setup.py sdist bdist_wheel --formats=zip

import setuptools
import os
import shutil
import sys

ROOT_PATH = os.path.abspath(os.path.dirname(__file__)) 

with open(f'{ROOT_PATH}/README.rst', 'r') as file:
    long_description = file.read()

project_name = "cmrsim"
author_list = "Jonathan Weine, Charles McGrath"
author_email_list = "weine@biomed.ee.ethz.ch, mcgrath@biomed.ee.ethz.ch"
url = "https://gitlab.ethz.ch//ibt-cmr/mri_simulation/cmrsim/"

project_urls = {
    'Documentation': 'https://people.ee.ethz.ch/~jweine/cmrsim/latest/index.html',
    'Source': 'https://gitlab.ethz.ch//ibt-cmr/mri_simulation/cmrsim/',
    'Institute': 'https://cmr.ethz.ch/'
}

# Get version tag
if '--version' in sys.argv:
    tag_index = sys.argv.index('--version') + 1
    current_version = sys.argv[tag_index]
    sys.argv.pop(tag_index-1)
    sys.argv.pop(tag_index-1)
else:
    raise ValueError('No version as keyword "--version" was specified')

with open(f'{project_name}/__init__.py', 'r+') as module_header_file:
    content = module_header_file.read()
    module_header_file.seek(0)
    module_header_file.write(f"__version__ = '{current_version}'\n" + content)

extras = {
    "cuda": ["tensorflow[and-cuda]==2.15.1", ],
    # "phantoms": [] Planned for future installation of resources
}

setuptools.setup(
    name=project_name,
    url=url,
    project_urls=project_urls,
    version=current_version,
    author=author_list,
    author_email_=author_email_list,
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=["tensorflow==2.15.1", "pyvista>=0.42", "numpy>=1.22", "pint>=0.18", "cmrseq>=0.23"],
    extras_require=extras,
    python_requires=">=3.6"
)
