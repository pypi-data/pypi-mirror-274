from setuptools import setup, find_packages


setup(
    name="twinlib",
    version="0.1.7",
    author="gaiamzz",
    author_email="mzzgai@unife.it",
    description="A library for twin detection",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'twinlib = twinlib_pkg:hello'
        ]
    },
    packages=find_packages(),
    install_requires=[],
    extras_require={},
)
