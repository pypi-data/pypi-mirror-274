from setuptools import find_packages, setup
setup(
    name='MT5LinuxEnhanced',
    packages=find_packages(include=['mt5linux']),
    version='0.3.1',
    description='MetaTrader5 for Linux users, improved version',
    long_description=open('README.md','r').read(),
    long_description_content_type='text/markdown',
    author='Lucas Prett Campagna, Renan Ribeiro Lage',
    license='MIT',
    url = 'https://github.com/kusmin/MT5LinuxEnhanced',
    install_requires=open('requirements.txt','r').read().split('\n'),
    setup_requires=[],
    tests_require=[],
    test_suite='tests',
)
