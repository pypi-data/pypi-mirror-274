from setuptools import setup, find_packages
with open('README.md', 'r') as f:
          readme =f.read()

setup(
    name='blaze_double_bot',
    licence='MIT License',
    version='0.1.2',
    author='Rafael de Oliveira Ribeiro',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='ror74559@gmail.com',
    description='This Python library automates the betting process on the Blaze Double',
    packages=['blaze_double_bot'],
    install_requires=[
        'undetected_chromedriver',
        'selenium',
        'requests'
    ],
   
)

