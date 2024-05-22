from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='tmticket',
    version='0.2.17',
    author='hokiebrian',
    author_email='hokiebrian@gmail.com',
    description="Python wrapper for the Ticketmaster Discovery API",
#    long_description=read('README.rst'),
    license='MIT',
    keywords='Ticketmaster',
    url='https://github.com/hokiebrian/pytmtickets',
    packages=['tmticket'],
    install_requires=['requests']
)