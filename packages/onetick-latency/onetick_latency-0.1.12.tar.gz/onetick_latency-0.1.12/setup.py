from setuptools import setup, find_packages

# Safely read the long description from 'README.md'
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='onetick_latency',
    version='0.1.12',
    description='Library for latency simulation and query for Onetick',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alexandre Levert',
    author_email='alexandre.levert.1@bnc.ca',
    url='https://gitlab.awsged.com/bigdata/onetick_latency.git',
    packages=find_packages(include=['onetick_latency*', 'modules*', 'pythonAPI*']),
    install_requires=[
        'numpy',
        'pandas',
        'onetick'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
