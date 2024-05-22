from setuptools import setup, find_packages

setup(
    name='jzpypi',
    version='50.37.49',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'tqdm',
        'requests-toolbelt',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'jzpypi = jzpypi.upload:main',
        ],
    },
)
