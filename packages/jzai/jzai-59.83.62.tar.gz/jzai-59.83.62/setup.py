from setuptools import setup, find_packages

setup(
    name='jzai',
    version='59.83.62',
    packages=find_packages(),
    package_data={'jzai': ['jzai/conversations.json']},
    install_requires=[
        'numpy',
        'pyttsx3',
        'speechrecognition',
        'nltk',
        'textblob',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jzai=jzai.cli:run',
        ],
    },
)
