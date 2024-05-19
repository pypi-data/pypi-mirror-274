from setuptools import setup, find_packages # type: ignore

setup(
    name='WeatherPlug',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        
        'Requests>=2.31.0'
    ],
)