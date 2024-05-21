from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='jesse-apexpro',
    version='1.0.0',
    packages=find_packages(),
    description='Python3 Apexpro HTTP/WebSocket API Connector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/saleh-mir/apexpro-openapi',
    license='MIT License',
    author='Saleh Mir',
    author_email='saleh@jesse.trade',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='apexpro api connector',
    package_data={'': ['*.json']},
    data_files=[('apexpro', ['apexpro/starkex/starkex_resources/pedersen_params.json'])],
    # packages=['apexpro'],
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'websocket-client',
        'websockets',
        'dateparser==1.0.0',
        'ecdsa==0.16.0',
        'eth_keys',
        'eth-account>=0.4.0,<0.9.0',
        'mpmath==1.0.0',
        'sympy==1.6',
        'tox',
        'web3==6.10.0',
    ],
)
