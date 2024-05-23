from setuptools import setup, find_packages

setup(
    name='vocabulary_quiz',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'requests',
        'beautifulsoup4',
        'csv',
    ],
    entry_points={
        'console_scripts': [
            'run-vocabulary-quiz=run:main',
        ],
    },
)
