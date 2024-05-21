from setuptools import setup, find_packages

setup(
    name='testsegmtor', 
    version='0.0.1',   
    packages=find_packages(), 
    install_requires=[
        'numpy',                 
    ],
    author='Beijuka Bruno',            
    author_email='beijukab@gmail.com',  
    description='Preprocessing of images for OCR',  
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

