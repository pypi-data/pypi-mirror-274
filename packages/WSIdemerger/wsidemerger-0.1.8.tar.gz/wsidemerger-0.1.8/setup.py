
from setuptools import setup, find_packages
import os

def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except FileNotFoundError:
        return ""

setup(
    name='WSIdemerger',
    version='0.1.8',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openslide-python',
        'Pillow',
        'numpy',
        'scikit-image',
        'tqdm',
        'opencv-python',
        'staintools'
    ],
    author='Thirteen',
    author_email='506607814@qq.com',
    description='A package for extracting image patches from SVS files and performing color normalization',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/WSI_Preprocessing',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
