from setuptools import setup, find_packages

setup(
    name='mgolddepthlib',
    version='0.2',
    packages=find_packages(include=['mylib', 'util', 'model']),
    description='Marigold Depth',
    author='Marigold',
    license='MIT',
)