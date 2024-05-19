from setuptools import setup, find_packages
import os
import re

def get_version():
    init_py_path = os.path.join(os.path.dirname(__file__), 'rikibot', '__init__.py')
    with open(init_py_path, 'r') as f:
        for line in f:
            match = re.match(r"__version__\s*=\s*['\"](.*?)['\"]", line)
            if match:
                return match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="rikibot",
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="A simple Python package named rikibot.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vu Nguyen",
    author_email="anhvusg.it@gmail.com",
    url="https://github.com/anhvu-sg/rikibot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'rikibot=rikibot.__main__:main',
        ],
    },
)
