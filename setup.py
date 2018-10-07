from setuptools import setup, find_packages

setup(
    name='YouTube-Loader',
    description='Download tool for multiple YouTube videos.',
    author='Alex Hall',
    author_email='alexhall93@me.com',
    version=0.2,
    url='https://github.com/hallcode/yt-loader',
    packages=find_packages(),
    python_requires='>=3',
    include_package_data=False,
    install_requires=[
        'click',
        'clint',
        'pytube'
    ],
    entry_points={
        'console_scripts': [
            'yt-loader = loader.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)