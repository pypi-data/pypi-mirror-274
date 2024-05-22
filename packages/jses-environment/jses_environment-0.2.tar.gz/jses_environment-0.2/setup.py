from setuptools import setup, find_packages

setup(
    name='jses_environment',
    version='0.2',
    packages=['jsesEnv'],
    install_requires=[],
    url='https://github.com/joseaugustoduarte/jses_environment.git',
    license='MIT License',
    author='José Augusto Duarte',
    author_email='joseaugustoduarte@gmail.com',
    description='Esse pacote cria um ambiente no Google Colab para quem deseja trabalhar com Spark e ElasticSearch.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown')