from setuptools import setup

setup(
    name='csmas',
    version='0.0.1',
    packages=['csmas'],
    entry_points={
        'console_scripts': [
            'csmas=your_package.__init__:main',
        ],
    },
)