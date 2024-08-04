from setuptools import setup, find_packages

setup(
    name='popsim',
    version='0.1.0',
    author='Khanh Duy Nguyen',
    author_email='kduyng71@gmail.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/indexlab/popsim',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)