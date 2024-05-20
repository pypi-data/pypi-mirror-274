from setuptools import setup, find_packages

setup(
    name='clean_data_python',
    version='0.1.0',
    description='A package for handling various data preprocessing tasks',
    author='murat & ahmet & cagla',
    author_email='murat.keskin@stu.fsm.edu.tr',
    url='https://github.com/MuratKeskin0/Python_Data_Cleaning',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        # Add other dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)