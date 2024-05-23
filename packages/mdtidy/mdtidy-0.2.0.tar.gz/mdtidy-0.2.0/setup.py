from setuptools import setup, find_packages

setup(
    name='mdtidy',
    version='0.2.0',
    description='A Python library to clean and format markdown content into Jupyter Notebooks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='David Jeremiah',
    author_email='flasconnect@gmail.com',
    url='https://github.com/davidkjeremiah/mdtidy',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)