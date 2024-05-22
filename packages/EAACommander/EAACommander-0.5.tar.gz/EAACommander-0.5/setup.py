from setuptools import setup, find_packages

setup(
    name='EAACommander',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'art',
    ],
    entry_points={
        'console_scripts': [
            'eaacommander=EAACommander.cli_client:main_entry_point',
        ],
    },
    package_data={
        'EAACommander': ['settings.ini'],
    },
    include_package_data=True,
    author='Marko Žnidar',
    author_email='marko.znidar@gmail.com',
    description='A tool for Electronically Assisted Astronomy (EAA) enthusiasts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MarkoZnidar/EAACommander/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
