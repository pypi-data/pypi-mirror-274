from setuptools import setup, find_packages

setup(
    name='suse_udfs_cyy',
    version='0.1.1',
    packages=find_packages(),
    description='A useful tool for extracting data using WindPy',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    author='YaoyuChenWilliam',
    author_email='yaoyuchenslm@gmail.com',
    license='MIT',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
