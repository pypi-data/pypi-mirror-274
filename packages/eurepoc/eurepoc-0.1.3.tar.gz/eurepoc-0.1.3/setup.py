from setuptools import setup, find_packages

setup(
    name='eurepoc',
    version='0.1.3',
    author='Camille Borrett',
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
    install_requires=[
        'requests>=2.31.0,<3.0.0',
        'nested_query_string>=0.0.1,<0.1.0',
        'pandas>=2.2.2,<3.0.0',
        'pydantic>=2.7.1,<3.0.0'
    ],
    python_requires='>=3.6',
)
