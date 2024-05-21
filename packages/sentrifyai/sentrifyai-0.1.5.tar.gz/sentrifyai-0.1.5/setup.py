from setuptools import setup, find_packages

setup(
    name='sentrifyai',
    version='0.1.5',
    description='SentrifyAI API client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SentrifyAI',
    author_email='admin@sentrify.org',
    url='https://github.com/sentrifybot/sentrifyai-python',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    namespace_packages=['sentrifyai'],
)