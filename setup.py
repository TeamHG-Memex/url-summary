import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='url-summary',
    version='0.0.3',
    author='Konstantin Lopuhin',
    author_email='kostia.lopuhin@gmail.com',
    description='Display a summary of urls in a notebook',
    license='MIT',
    url='https://github.com/TeamHG-Memex/url-summary',
    packages=['url_summary'],
    install_requires=[
        'six',
        'typing',
    ],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
