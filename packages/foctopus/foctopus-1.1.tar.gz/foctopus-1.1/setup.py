from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='foctopus',
    version='1.1',
    author='ForestBu',
    author_email='tvc55.admn@gmail.com',
    description='Many functions for python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/ForestBu/foctopus',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='login password logout reg register regitration functions pause time sleep stop shell',
    python_requires='>=3.11'
)
