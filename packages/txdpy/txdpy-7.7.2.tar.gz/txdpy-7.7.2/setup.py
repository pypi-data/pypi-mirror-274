from distutils.core import setup
import setuptools
packages = ['txdpy']
setup(name='txdpy',
    version='7.7.2',
    author='唐旭东',
    packages=packages,
    package_dir={'requests': 'requests'},
    install_requires=[
        "lxml","loguru","tqdm","colorama","openpyxl","pymysql","xlsxwriter","selenium","natsort","sshtunnel","file_ls","requests","xlrd"
    ])