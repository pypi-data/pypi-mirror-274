from setuptools import setup, find_packages

setup(
    name='vin-validator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Tobias Lieshoff',
    author_email='me@tobias-lieshoff.de',
    description='A package to validate Vehicle Identification Numbers (VINs)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tlieshoff/vin-validator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
