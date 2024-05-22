from setuptools import setup, find_packages

setup(
    name='setup_django_apex',
    version='0.1.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'setup_django_apex=setup_django_apex.installer:main'
        ],
    },
    install_requires=[
        'django',
    ],
)
