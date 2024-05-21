from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pyresumeparser',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pdfminer.six==20231228',
        'spacy==3.7.4',
        'spacy-transformers==1.3.5'
    ],
    package_data={
        'resume_parser': ['model-best/*']
    },
    entry_points={
        'console_scripts': [
            'pyresumeparser=resume_parser.main:main',
        ],
    },
    author='Palash Khan',
    author_email='palashkhan777@gmail.com',
    description='A package for parsing resume and extracting entities.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pkhan123/resume_parser',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
