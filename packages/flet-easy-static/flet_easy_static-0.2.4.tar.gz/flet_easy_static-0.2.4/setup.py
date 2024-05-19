from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='flet_easy_static',
    version='0.2.4',
    packages=find_packages(),
    install_requires=[
        'PyJWT'
        # 'flet',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)