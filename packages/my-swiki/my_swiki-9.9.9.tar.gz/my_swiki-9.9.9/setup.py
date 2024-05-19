from setuptools import setup

setup(
    name='my_swiki',
    version='9.9.9',
    description='A program for searching and reading Wikipedia articles in multiple languages',
    py_modules=['myswiki'],
    author='k0ng999',
    author_email='baydar_14@mail.ru',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)
