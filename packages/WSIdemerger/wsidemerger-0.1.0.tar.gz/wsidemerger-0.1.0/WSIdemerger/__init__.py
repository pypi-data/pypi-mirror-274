from setuptools import setup, find_packages

setup(
    name='WSIdemerger',
    version='0.1.0',
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
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/WSI_Preprocessing',  # 替换为你的GitHub仓库地址
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
