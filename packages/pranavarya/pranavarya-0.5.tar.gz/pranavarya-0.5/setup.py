from setuptools import setup, find_packages

setup(
    name='pranavarya',
    version='0.5',
    author='Pranav Arya',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'pranavarya=pranavarya.main:hello'
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)