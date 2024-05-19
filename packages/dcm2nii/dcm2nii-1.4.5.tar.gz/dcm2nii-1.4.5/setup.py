from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dcm2nii',
    version='1.4.5',
    url='https://github.com/cnnlabyzu/dicom2nifti',
    author='Wei-Chun Kevin Tsai',
    author_email='cnnlabproject@gmail.com',
    description='A simple python 3rd package application for DICOM to NIfTI conversion.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.4',
        'pydicom==2.0.0',
        'tqdm==4.66.2',
        'nibabel==4.0.2'
    ],
)