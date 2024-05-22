from setuptools import setup, find_packages

setup(
    name='secbulkdownload',  # New name for your package
    version='0.0.1',  # Update the version as needed
    author='kuatroka',
    author_email='your.email@example.com',
    description='A modified version of sectoolkit',
    url='https://your-repository-url',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your package needs
'bs4==0.0.2',
'pandas==2.2.2',
'tqdm==4.66.4',
'xmltodict==0.13.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
