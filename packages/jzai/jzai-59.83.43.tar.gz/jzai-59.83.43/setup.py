from setuptools import setup, find_packages

setup(
    name='jzai',
    version='59.83.43',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pyttsx3',
        'speechrecognition',
        'nltk',
        'textblob',
        'click',
        'pwinput'
    ],
    entry_points={
        'console_scripts': [
            'jzai=jzai.cli:run',
        ],
    },
)
