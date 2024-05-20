from setuptools import setup, find_packages

setup(
    name='pymtr',
    version='1.0.1',
    description='A Python process monitoring tool',
    author='Artem Bolshakov',
    author_email='artemis4650@gmail.com',
    packages=find_packages(),
    install_requires=[
        'psutil',  # Add any dependencies here
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'pymtr = pymtr.main:main',  # Entry point for command-line usage
        ],
    },
)

