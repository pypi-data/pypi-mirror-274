# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['madokami',
 'madokami.api',
 'madokami.drivers',
 'madokami.internal',
 'madokami.internal.default_plugins',
 'madokami.plugin',
 'madokami.plugin.backend']

package_data = \
{'': ['*']}

install_requires = \
['apscheduler>=3.10.4,<4.0.0',
 'aria2p>=0.12.0,<0.13.0',
 'fastapi>=0.110.1,<0.111.0',
 'loguru>=0.7.2,<0.8.0',
 'pydantic>=2.7.0,<3.0.0',
 'pytest-xdist>=3.5.0,<4.0.0',
 'pytest>=8.1.1,<9.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'requests>=2.31.0,<3.0.0',
 'sqlalchemy>=2.0.29,<3.0.0',
 'sqlmodel>=0.0.16,<0.0.17',
 'uvicorn>=0.29.0,<0.30.0']

setup_kwargs = {
    'name': 'madokami',
    'version': '0.1.3',
    'description': 'A core library for madokami',
    'long_description': 'Madokami项目的核心库',
    'author': 'Hongpei Zheng',
    'author_email': 'summerkirakira@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
