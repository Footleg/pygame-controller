from setuptools import setup, find_packages

setup(
    name="PygameController",
    version="1.0",
    packages=find_packages(where="."),
    
    install_requires=["pygame>=1.9"],
    
    # metadata to display on PyPI
    author="Paul 'Footleg' Fretwell",
    author_email="drfootleg@gmail.com",
    description="Helper class to interface robots to game controllers on the Raspberry Pi.",
    keywords="Raspberry Pi Robotics",
    url="https://github.com/Footleg/pygame-controller/",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development"
    ]
)