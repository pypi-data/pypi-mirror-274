from setuptools import setup, find_packages

setup(
    name='my_trino_lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'trino'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for connecting to Trino and performing SQL operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_trino_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
