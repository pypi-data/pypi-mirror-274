
import setuptools
from setuptools import setup, find_packages

#with open("README.md", 'r', encoding='utf-8') as f:
    #long_description = f.read()
with open("README.md") as readme:
    long_description = readme.read()    
    
setup(
    name='nz_seqtech',
    version='0.2.11',
    license='Apache',
    description='A library for DNA sequence encoding in quantum machine learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url ='https://nz-seqtech.com/',
    author='Nouhaila Innan and Muhammad Al-Zafar Khan',
    author_email='nouhaila.innan@zaiku.com, muhammad.khan@zaikugroup.com',
    packages=find_packages(),
    install_requires=[
    'wheel',    
    'numpy>=1.20.0',
    'pandas>=1.2.0',
    'scikit-learn>=0.24.0',
    'qiskit==0.43.1',
    'matplotlib>=3.3.4',
    'qiskit-algorithms',
    'qiskit-machine-learning==0.6.1',
    'qiskit-aer==0.12.0',
    'qiskit-ibmq-provider==0.20.2'   
    ],
    project_urls={
        'Documentation': 'https://nz-seqtech.readthedocs.io/',
    },
)
