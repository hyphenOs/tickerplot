from setuptools import setup, find_packages
import os

from tickerplot import __version__
print __version__
version = __version__

curdir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(curdir,'requirements.txt')) as f:
    all_reqs = f.read().split('\n')

install_requires = [ x.strip() for x in all_reqs if (not x.startswith('#'))]
print install_requires

dependency_links=install_requires

setup(name='tickerplot',
        version=version,
        description='tickerplot Common Utility Functions',
        url='https://github.com/gabhijit/tickerplot',
        license='MIT',
        classifiers=[
            'Natural Language :: English',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
        ],
        keywords='stocks NSE',
        packages=find_packages(exclude=['venv', 'venv3']),
        include_package_data=True,
        install_requires=install_requires,
        dependency_links=dependency_links,
        author='Abhijit Gadgil',
        author_email='gabhijit@iitbombay.org'
    )

