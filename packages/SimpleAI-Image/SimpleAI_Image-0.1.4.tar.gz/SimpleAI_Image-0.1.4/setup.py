from setuptools import setup, find_packages

setup(
    name='SimpleAI_Image',  # Change this to a unique name
    version='0.1.4',  # Increment the version number
    description='A package for processing and storing image vectors in PostgreSQL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tobias Poulsen',
    author_email='your.email@example.com',
    url='https://github.com/Tobias2408/bachelorprojekt',  # Your package's URL
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'pandas==1.5.3',
        'sqlalchemy==2.0.30',
        'matplotlib==3.6.3',
        'tensorflow-macos==2.12.0',  # Updated to the latest available version
        'tensorflow-datasets==4.9.2',
        'tensorflow-metal==0.8.0',
        'scikit-learn==1.2.2',
        'requests==2.31.0',
        'keras==3.0.0',
        'tensorboard==2.16.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
