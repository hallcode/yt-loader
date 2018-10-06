from setuptools import setup, find_packages

setup(
    name='greet',
    version=0.1,
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'click',
        'clint',
        'pytube'
    ],
    entry_points={
        'console_scripts': [
            'yt-loader = loader.loader:main'
        ]
    }
)