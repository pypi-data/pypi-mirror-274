"""setup tools usage to make packages"""

from setuptools import setup, find_packages
import wheel

setup(
    name='package_iiii',
    version='0.0.1',
    packages=find_packages(),
    author='Satyam Nyati',
    author_email='sam.28011997@gmail.com',
    description='A module to calculate math',
    license='MIT',
    install_requires=[
        'pandas',
        'numpy'
    ],
    setup_requires=[
        'wheel'
    ]
)
