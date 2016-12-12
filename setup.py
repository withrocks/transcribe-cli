"""
Transcribe audio text on the command line
"""
from setuptools import find_packages, setup

dependencies = ['click']

setup(
    name='transcribe_cli',
    version='0.1.0',
    url='https://github.com/withrocks/transcribe-cli',
    author='Steinar Sturlaugsson',
    author_email='withrocks@noreply.github.com',
    description='Transcribe audio text on the command line',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'transcribe-cli = transcribe_cli.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
