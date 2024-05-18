from setuptools import setup, find_packages

setup(
    name='eloz-space',  # Unique project name
    version='1.1',  # Incremented version number
    author='eL0z',
    author_email='your.email@example.com',
    description='A tool to display storage information',
    long_description='This package provides information about storage space.',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/eloz-space',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'space=space.space:main',
        ],
    },
    install_requires=[
        'psutil',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
