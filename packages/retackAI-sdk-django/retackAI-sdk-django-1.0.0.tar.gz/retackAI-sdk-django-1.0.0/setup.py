from setuptools import setup, find_packages

setup(
    name='retackAI-sdk-django',
    version='1.0.0',
    description='Retack SDK for Django',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Truenary',
    author_email='contact@truenary.com',
    url='https://github.com/truenary/retack_pkg_python',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests']
)
