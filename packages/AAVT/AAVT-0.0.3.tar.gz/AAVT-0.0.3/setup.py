from setuptools import setup, find_packages

setup(
    name='AAVT',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'faster-whisper',
        'openai',
        'opencv-python',
    ],
    description='A Python package for Video Translate and Some Tools for Video',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='chenyme（Orange橙子）',
    author_email='chenyme03@gmail.com',
    url='https://github.com/Chenyme/Chenyme-AAVT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

