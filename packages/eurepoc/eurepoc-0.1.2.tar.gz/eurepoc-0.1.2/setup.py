from setuptools import setup, find_packages

setup(
    name='eurepoc',
    version='0.1.2',
    author='Camille Borrett',
    author_email='camille.borrett@posteo.net',
    description='Wrapper for the EuRepoC API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Documentation': 'https://eurepoc.readthedocs.io/',
        'Source': 'https://github.com/camilleborrett/eurepoc',
        'Tracker': 'https://github.com/camilleborrett/eurepoc/issues',
        'EuRepoC Project': 'https://eurepoc.eu/'
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'nested_query_string', 'pandas', 'datetime', 'pydantic', 'typing'],
    python_requires='>=3.6',
)
