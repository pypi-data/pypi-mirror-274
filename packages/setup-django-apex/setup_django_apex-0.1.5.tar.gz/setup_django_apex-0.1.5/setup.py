from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call(['python', '-m', 'setup_django_apex.installer'])

setup(
    name='setup_django_apex',
    version='0.1.5',
    author='Anirudha Udgirkar',
    author_email='anirudhaudgirkar.work.email@example.com',
    description='A library to set up Django projects with multiple apps',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Anirudha1821/setup_django_apex',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django>=3.0',
        'django>=3.0',
    ], 
    extras_require={
        'tests': ['pytest'],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
