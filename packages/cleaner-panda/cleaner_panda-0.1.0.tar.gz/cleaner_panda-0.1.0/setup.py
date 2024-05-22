from setuptools import setup, find_packages

setup(
    name='cleaner_panda',
    version='0.1.0',
    description='A package for handling various data preprocessing tasks',
    author='asimtarik & emirs',
    author_email='support@cleanpanda.com',
    url='https://github.com/EmirhanSyl/cleaner-panda',
    download_url='https://github.com/EmirhanSyl/cleaner-panda/archive/refs/tags/v0.1.0.tar.gz',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk'
        'category_encoders'
        'scipy'
        'bs4'
        'contractions'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)