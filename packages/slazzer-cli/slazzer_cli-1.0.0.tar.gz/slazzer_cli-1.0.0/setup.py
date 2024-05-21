from setuptools import setup, find_packages

setup(
    name='slazzer-cli',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'slazzer-cli=slazzer_cli:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool for removing backgrounds using the Slazzer API.',
    url='https://github.com/yourusername/slazzer-cli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
