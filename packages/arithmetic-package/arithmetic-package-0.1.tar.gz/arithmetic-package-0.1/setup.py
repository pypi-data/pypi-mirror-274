from setuptools import setup, find_packages

setup(
    name='arithmetic-package',
    version='0.1',
    packages=find_packages(),  # This should find the 'arithmetic' package
    description='A simple package for basic arithmetic operations using functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/arithmetic-package',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
