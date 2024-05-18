from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dicom2image',
    version='1.3.5',
    url='https://github.com/cnnlabyzu/dicom2image',
    author='Wei-Chun Kevin Tsai',
    author_email='cnnlabproject@gmail.com',
    description='A simple python 3rd package application for DICOM to image conversion.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'opencv-contrib-python==4.9.0.80',
        'tqdm==4.66.2',
        'pylibjpeg-libjpeg==1.3.0',
        'pydicom==2.0.0'
    ],
)
