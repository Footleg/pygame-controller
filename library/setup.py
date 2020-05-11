from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pygame-controller",
    version="0.1.0",
    packages=find_packages(),
    
    install_requires=["pygame>=1.9"],
    
    # metadata to display on PyPI
    author="Paul 'Footleg' Fretwell",
    author_email="drfootleg@gmail.com",
    description="Helper class to interface robots to game controllers on the Raspberry Pi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Raspberry Pi Robotics",
    url="https://github.com/Footleg/pygame-controller/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development"
    ],
    python_requires='>=3.6',
)