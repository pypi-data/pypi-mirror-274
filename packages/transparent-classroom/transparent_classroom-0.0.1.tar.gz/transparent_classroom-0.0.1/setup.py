from setuptools import setup, find_packages

setup(
    name='transparent_classroom',
    version='0.0.1',
    author='Dylan Pozorski',
    author_email='dylanpozorski@gmail.com',
    url='https://github.com/dpozorski/transparent-classroom',
    description="Python Client for accessing Transparent Classroom's data model.",
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'setuptools',
        'pytz',
        'requests'
    ]
)
