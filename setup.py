from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='directusDK',  # This is the name of the of the sdk
    version='1.0',  
    packages=find_packages(),
    install_requires=requirements,  # Here we use the contents of requirements.txt
    author='peskyAdmin',
    author_email='peskyAdmin@pm.me',
    description='A Simple Directus SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/peskyAdmin/DirectusDK',
    license='MIT',
)