from setuptools import setup, find_packages

setup(
    name="rikibot",
    version="0.1.0",
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
)
