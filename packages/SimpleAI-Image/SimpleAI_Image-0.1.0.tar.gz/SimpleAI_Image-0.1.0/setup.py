from setuptools import setup, find_packages

setup(
    name='SimpleAI_Image',  # Change this to a unique name
    version='0.1.0',
    description='A package for processing and storing image vectors in PostgreSQL',
    author='Tobias Poulsen',
    author_email='your.email@example.com',
    url='https://github.com/Tobias2408/bachelorprojekt',  # Your package's URL
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'sqlalchemy',
        'pgvector',
        'matplotlib',
        'tensorflow',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
