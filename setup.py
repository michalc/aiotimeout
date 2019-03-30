import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='aiotimeout',
    version='0.0.0',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='Timeout context manager for asyncio Python',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/aiotimeout',
    py_modules=[
        'aiotimeout',
    ],
    python_requires='~=3.5',
    tests_require=[
        'aiofastforward==0.0.24',
    ],
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
    ],
)
