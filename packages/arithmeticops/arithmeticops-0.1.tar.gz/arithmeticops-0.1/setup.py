from setuptools import setup, find_packages

setup(
    name='arithmeticops',
    version='0.1',
    packages=find_packages(),
    description='A simple package for basic arithmetic operations using classes and objects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='subidkumar.parida-EE@infineon.com',
    url='https://bitbucket.vih.infineon.com/scm/~paridasubidk/arithmeticops.git',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
