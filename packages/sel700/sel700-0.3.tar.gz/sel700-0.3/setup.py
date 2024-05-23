from setuptools import setup

with open('README.md', 'r') as arq:
    readme = arq.read()

setup(
    name='sel700',
    version='0.3',
    author='Elisandro Peixoto',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='SEL relays 700',
    description='Library to use Telnet commands in SEL relays 700 series',
    packages=['sel700'],
    install_requires=[]
)