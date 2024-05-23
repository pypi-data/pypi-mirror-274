from setuptools import setup, find_packages

setup(
    name='prmllab',
    version='0.4',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        'prmllab': ['files/*.txt', 'files/*.ipynb']
    },
)
