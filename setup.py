import setuptools


VERSION = 5


setuptools.setup(
    name="pypcs",
    version='0.0.' + str(VERSION),
    author="Jason Lee",
    author_email="2593292614@qq.com",
    description="",
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    install_package_data=True,
    package_data={'': ['*.txt', '*.md', '*.json', '*.png']},
    url="https://github.com/JasonLee-p/pyPCS",
    install_requires=[
        'numpy==1.24.2',
        'pygame==2.3.0',
        'rtmidi==2.5.0',
        'webcolors==1.12',
        'Pillow==9.5.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)
