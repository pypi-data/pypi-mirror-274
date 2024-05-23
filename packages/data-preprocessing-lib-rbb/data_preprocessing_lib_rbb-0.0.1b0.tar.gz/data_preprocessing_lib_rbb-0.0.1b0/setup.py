from setuptools import setup, find_packages

setup(
    name='data_preprocessing_lib_rbb',
    version='0.0.1-beta',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        'scikit-learn'
    ],
    author_name='Rafet Bartuğ',
    author_surname='Bartınlı',
    author_email='rafetbartug@gmail.com',
    description='A data preprocessing library in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rafetbartug',
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
