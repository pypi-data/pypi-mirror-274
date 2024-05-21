# setup.py

from setuptools import setup, find_packages

setup(
    name='lib-ml-remla-12',
    version='v0.1.8',  # Use a versioning scheme
    long_description=open('README.md').read(),
    packages=find_packages(),
    url='https://github.com/remla24-team12/lib_ml',
    install_requires=[
        "keras-preprocessing==1.1.2",
        "keras==3.2.1",
        "scikit-learn==1.4.2",
        "pandas==2.2.2"
    ],
    extras_requires={"dvc==3.50.1": ["gdrive"]}
)
