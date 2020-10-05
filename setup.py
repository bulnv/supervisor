import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="supervisor-demo", 
    version="0.0.1",
    author="Nikolai Bulashev",
    author_email="nvbulashev@gmail.com",
    description="A small pinguin lifter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bulnv/supervisor",
    packages=[
        subprocess,
        logging,
        argparse,
        shlex,
        os,
        time
    ]
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)