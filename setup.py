from setuptools import setup, find_packages

setup(
    name='jarvis',
    version='0.1',
    description='use ur voice',
    url='https://github.com/aryanmisra/jarvis',
    author='Aryan Misra',
    author_email='aryanmisra4@gmail.com',
    license='MIT',
    install_requires=['SpeechRecognition'],
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['jarvis=src.main:mic_test']
    )
)