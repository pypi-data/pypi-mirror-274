from setuptools import setup, find_packages

setup(
    name='RNASQLite',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'RNASQLite=RNASQLite.cli:main',
        ],
    },
    description='A tool for managing RNA-Seq data with SQLite',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/RNASQLite',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
