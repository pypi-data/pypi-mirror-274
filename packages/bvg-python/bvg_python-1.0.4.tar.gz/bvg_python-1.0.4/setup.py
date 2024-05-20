from setuptools import setup, find_packages

setup(
    name='bvg-python',
    version='1.0.4',
    description='Python wrapper for the BVG (Berliner Verkehrsbetriebe) public transportation REST API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tobias Lieshoff',
    author_email='me@tobias-lieshoff.de',
    url='https://github.com/tlieshoff/bvg-python',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
