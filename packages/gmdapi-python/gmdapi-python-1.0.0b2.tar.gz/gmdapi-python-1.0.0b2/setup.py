from setuptools import setup, find_packages

setup(
    name='gmdapi-python',
    version='1.0.0b2',
    description='GDAPI is a simple Python Geometry Dash API module.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Xytriza',
    author_email='cryfxreal@gmail.com',
    url='https://github.com/Xytriza/gmdapi-python',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
