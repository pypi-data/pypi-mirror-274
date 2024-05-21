from setuptools import setup, find_packages

setup(
    name='RACHUS',
    version='0.1.0',
    packages=find_packages(),
    description='A custom encryption library that compresses data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Rey',
    author_email='rey@cock.lu',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
