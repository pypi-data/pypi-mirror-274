from setuptools import setup, find_packages

setup(
    name='cleanerPandasVol',
    version='0.1.3',
    author='Murat Keskin & Ahmet Bagbakan & Cagla Ilhani',
    author_email='eng.murat.keskin@gmail.com',
    description='A comprehensive Python library for data preprocessing and cleaning',
    url='https://github.com/MuratKeskin0/Python_Data_Project_Vol',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'nltk',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)