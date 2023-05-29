import os
from typing import List

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


def read_requirements(
        file_name: str
) -> List:
    """
    Read requirements.txt file and return list of requirements.
    """
    with open(
            os.path.join(
                os.path.dirname(__file__),
                file_name
            )
    ) as f:
        return f.read().splitlines()


setup(
    name='selenite',
    version='1.0.0',
    author='xgu',
    author_email='g_xin@outlook.com',
    description='python + pytest + selene + allure automation test project',
    long_description=long_description,
    packages=find_packages(exclude=['test*', 'examples']),
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8, <3.11',
)
