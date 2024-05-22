from setuptools import setup, find_packages

setup(
    name='datacleanerpandas',
    version='0.1.0',
    description='A package for handling various data preprocessing tasks',
    author='baharkarakas & AlperCna',
    author_email='support@pandasdatacleaner.com',
    url='https://github.com/baharkarakas/datacleanerpandas',
    download_url='https://github.com/baharkarakas/datacleanerpandas/archive/refs/tags/v0.1.0.tar.gz',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk',
        'category_encoders',
   ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)