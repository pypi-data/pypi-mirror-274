# setup.py

from setuptools import setup, find_packages

setup(
    name='preprocessinglib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk'
    ],
    author='Zehra Tonga-Ayse Serra Gumustakim',
    author_email='tongafatmazehra@gmail.com-ayseserra.gumustakim@stu.fsm.edu.tr ',
    description='A comprehensive data preprocessing library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Fzehzeh/mypreprocessinglib , https://github.com/ayserragm/mypreprocessinglib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
