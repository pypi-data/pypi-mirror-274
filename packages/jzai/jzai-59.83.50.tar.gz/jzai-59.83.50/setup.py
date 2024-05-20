from setuptools import setup, find_packages

setup(
    name='jzai',
    version='59.83.50',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyttsx3',
        'speechrecognition',
        'nltk',
        'textblob',
        'click',
        'pwinput',
        'aiofiles',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'jzai=jzai.cli:run',
        ],
    },
)
