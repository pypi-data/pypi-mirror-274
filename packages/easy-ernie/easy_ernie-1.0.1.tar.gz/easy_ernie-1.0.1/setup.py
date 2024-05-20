from setuptools import setup, find_packages

with open('./README.md', 'r', encoding='utf-8') as file:
    readMe = file.read()

setup(
    name='easy-ernie',
    version='1.0.1',
    description='简洁的调用文心一言的WebAPI',
    long_description=readMe,
    long_description_content_type='text/markdown',
    author='XiaoXinYo',
    url='https://github.com/XiaoXinYo/Easy-Ernie',
    packages=find_packages('./src'),
    license='MIT',
    package_dir={'': './src'},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.8'
)