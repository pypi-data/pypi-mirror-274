from setuptools import setup, find_packages

setup(
    name="yspscda",
    version="0.0.2",
    author="Priyansh Srivastava",
    author_email="spriyansh29@gmail.com",
    description="Yet Another Package for Single-Cell Data Analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/spriyansh/yspscda",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=[
        "pytest",
    ],
)
