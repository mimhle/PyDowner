from setuptools import setup, find_packages

setup(
    name="PyDowner",
    version="0.0.7",
    author="mimhle",
    author_email="lengocminh19092004@gmail.com",
    description="A simple downloader for Python",
    long_description="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "tqdm",
    ],
    python_requires=">=3.10",
)
