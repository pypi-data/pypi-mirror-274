# setup.py
from setuptools import setup, find_packages

setup(
    name='vocabulary_quiz',
    version='0.5',  # 여기서 버전 번호를 증가시킵니다.
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'vocabulary_quiz=App.__main__:main',
        ],
    },
)
