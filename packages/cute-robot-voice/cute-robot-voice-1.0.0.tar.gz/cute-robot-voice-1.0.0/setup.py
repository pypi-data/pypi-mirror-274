from setuptools import setup, find_packages

setup(
    name='cute-robot-voice',
    version='1.0.0',
    author='Tushar Raha',
    author_email='tusharraha552@gmail.com',
    description='A package for generating cute robot voices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tushar552/cute-robot-voice',
    packages=find_packages(),
    install_requires=[
        'gtts',
        'pydub',
        'numpy',
        'simpleaudio',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
