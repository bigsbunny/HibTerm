from setuptools import setup, find_packages

setup(
    name='HibTerm',
    version='1.0.0',
    author = 'Bighnesh Sahoo',
    author_email = 'bighnesh2001@gmail.com',
    description = 'HibTerm is a CLI tool for fetching notices from IIIT Bhubaneswar\'s official portal - M-UMS',
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'hibterm = mainfol.test:test',
        ],
    },
)