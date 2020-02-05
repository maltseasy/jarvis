from setuptools import setup, find_packages

setup(
    name='jarvis',
    version='0.1',
    description='Use your voice and tell Jarvis to do stuff.',
    url='https://github.com/aryanmisra/jarvis',
    author='Aryan Misra',
    author_email='aryanmisra4@gmail.com',
    license='MIT',
    install_requires=['SpeechRecognition'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['jarvis=src.main:bkgd_recog']
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu",
    ],
    python_requires='>=3.6'
)