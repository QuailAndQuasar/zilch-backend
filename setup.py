from setuptools import setup, find_packages

setup(
    name='zilch-backend',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'pytest',
        'httpx'
    ],
    entry_points={
        'console_scripts': [
            'zilch-backend=main:app',
        ],
    },
)
