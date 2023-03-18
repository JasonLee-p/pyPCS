import setuptools


VERSION = 5


setuptools.setup(
    name="pyPCS",
    version='0.0.' + str(VERSION),
    author="Jason Lee",
    author_email="2593292614@qq.com",
    description="",
    long_description="text/markdown",
    url="https://github.com",
    # requires=['numpy', 'pygame'],
    install_requires=['numpy', 'pygame'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
