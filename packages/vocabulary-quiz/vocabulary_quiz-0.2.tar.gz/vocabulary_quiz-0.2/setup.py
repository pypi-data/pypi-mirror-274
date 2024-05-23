# setup.py
from setuptools import setup, find_packages

setup(
    name='vocabulary_quiz',
    version='0.2',  # Update the version here
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'vocabulary-quiz=App.app:run'
        ]
    },
)
