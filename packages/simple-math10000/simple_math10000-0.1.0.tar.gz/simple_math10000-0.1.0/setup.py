from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='simple_math10000',
    version='0.1.0',  # Initial development release
    packages=find_packages(),
    install_requires=[

    ],
    author='Merve',
    author_email='merve_demir@stu.fsm.edu.tr',
    license='MIT',
    description='A simple math library for basic arithmetic operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/meyvadem/my_data_preprocessor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)