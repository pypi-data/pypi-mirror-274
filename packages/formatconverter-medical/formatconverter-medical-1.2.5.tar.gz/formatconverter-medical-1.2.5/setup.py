from setuptools import setup, find_packages


setup(
    name='formatconverter-medical',
    version='1.2.5',
    description='A toolbox for converting medical imaging data between DICOM, NIfTI, and image formats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Wei-Chun Kevin Tsai',
    author_email='cnnlabproject@gmail.com',
    url='https://github.com/cnnlabyzu/formatconverter',
    packages=find_packages(),
    install_requires=[
        'SimpleITK==2.2.1',
        'tqdm==4.66.2',
        'pydicom==2.0.0',
        'opencv-contrib-python==4.9.0.80',
        'numpy==1.24.3',
        'nibabel==4.0.2',
        'matplotlib==3.5.3'
    ]
)

