from setuptools import setup, find_packages
import os

# 获取 README.md 文件的内容
def read_long_description():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as fh:
            return fh.read()
    except FileNotFoundError:
        return "Default long description if README.md is not found."

setup(
    name='WSIdemerger',
    version='0.1.4',
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
    long_description=read_long_description(),
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
