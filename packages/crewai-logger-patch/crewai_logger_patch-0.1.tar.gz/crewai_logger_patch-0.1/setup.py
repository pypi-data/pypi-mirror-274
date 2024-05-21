from setuptools import setup, find_packages

setup(
    name='crewai-logger_patch',
    version='0.1',
    author='theCyberTech',
    author_email='the_t3ch@pm.me',
    packages=find_packages(),
    install_requires=[
        'crewai',
        # other dependencies
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
