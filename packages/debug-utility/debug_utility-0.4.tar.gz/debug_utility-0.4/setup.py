from setuptools import setup, find_packages

setup(
    name='debug_utility',
    version='0.4',
    packages=find_packages(),
    description='common functions used while programming in python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hien Quoc',
    author_email='',
    url='',
    install_requires=[
        # List your project's dependencies here
        # e.g., 'requests>=2.23.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
