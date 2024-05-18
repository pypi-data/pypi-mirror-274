from setuptools import setup, find_packages

setup(
    name='SACMES_PYTHON_PACKAGE',
    version='0.6',
    packages=find_packages(where='SACMES_PYTHON_PACKAGE'),
    package_dir={'': 'SACMES_PYTHON_PACKAGE'},
    author='Matthew Wong',
    author_email='twong50@email.com',
    description='Description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mattywonger/SACMES_Python_Package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)