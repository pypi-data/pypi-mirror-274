from setuptools import setup, find_packages

setup(
    name='oguzhan_gokcekoca_preprocessing',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        'scikit-learn'
    ],
    author='Oğuzhanzi Ömerzi Tahazi',
    author_email='omerkumek03@gmail.com',
    description='A comprehensive data preprocessing library for Python.',
    url='https://github.com/yourusername/data_preprocessing_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
