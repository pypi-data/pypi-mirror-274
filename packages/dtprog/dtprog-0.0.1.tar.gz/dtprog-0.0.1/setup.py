from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='dtprog',
    version='0.0.1',
    description='Decision-theoretic Programming in Python',
    keywords = [],
    url='https://github.com/markkho/dtprog',
    author="Mark Ho",
    author_email='mark.ho.cs@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
