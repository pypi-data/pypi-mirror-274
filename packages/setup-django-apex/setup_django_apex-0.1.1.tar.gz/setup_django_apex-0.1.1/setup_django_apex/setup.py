from setuptools import setup, find_packages

setup(
    name='setup_django_apex',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'setup-django-apex = setup_django_apex.installer:main',
        ],
    },
)
