from setuptools import setup, find_packages

setup(
    name='kbitools',
    version='0.1.2',
    author='gizmokhan',
    description='Tools and rarely-changing modules for use with the kbi daemon.',
    packages=find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    install_requires=[
        'colorama>=0.4.4',  # And any other dependencies
        'requests>=2.31.0',
    ],
    entry_points={
        'console_scripts': [
            'kbicli = kbitools.klient:main',
        ],
    },
    python_requires=">=3.7",
)
