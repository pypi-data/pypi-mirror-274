from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mircheck",
    version="1.1.4",
    author="Arie Kurniawan",
    author_email="hubungi.aja@gmail.com",
    description="A tool to find the fastest mirror for Ubuntu and its derivatives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arkrwn/mircheck",
    packages=find_packages(),
    package_data={
        'mircheck': ['country-list.json'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'mircheck=mircheck.mircheck:main',
        ],
    },
)
