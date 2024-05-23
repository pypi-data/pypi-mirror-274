from setuptools import setup, find_packages

setup(
    name="vocabulary_quiz",
    version="0.3",  # 버전을 0.3으로 업데이트
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "requests",
        "beautifulsoup4"
    ],
    entry_points={
        'console_scripts': [
            'vocabulary_quiz=App.app:main',
        ],
    },
)
