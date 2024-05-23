from setuptools import setup, find_packages

setup(
    name='randombetter',
    version='1.0.2',
    author='Marek',
    author_email='marekciganik0603@gmail.com',
    description='a slowly developing randomness package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)