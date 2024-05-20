
from setuptools import setup, find_packages

setup(
    name='asyncCommunication',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'base64'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for handling HTTP requests with base64 encoding',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_python_library',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)