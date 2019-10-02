from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='unifipy',
    version='1.0.0',
    packages=[''],
    url='https://github.com/fronbasal/unifipy',
    license='MIT License',
    author='Daniel Malik',
    author_email='mail@fronbasal.de',
    description='Unifi Python API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
