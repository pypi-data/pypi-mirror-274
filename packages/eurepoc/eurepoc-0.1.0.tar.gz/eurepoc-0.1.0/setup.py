from setuptools import setup, find_packages

setup(
    name='eurepoc',
    version='0.1.0',
    author='Camille Borrett',
    author_email='camille.borrett@posteo.net',
    description='Wrapper for the EuRepoC API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/camilleborrett/eurepoc',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'nested_query_string', 'pandas', 'datetime', 'pydantic', 'typing'],
    python_requires='>=3.6',
)
