from setuptools import setup, find_packages
import os

version = '0.1.0'
long_description = open('README.txt').read()
classifiers = [
    "programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules"
]
setup(
    name='mai.bao',
    version=version,
    description='this is maidi package templates.',
    long_description=long_description,
    classifiers=classifiers,
    keywords='paste templates',
    author='MaiDi',
    author_email='15920164078@163.com',
    url='https://github.com/Maidi1990/my_bao_template',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['mai'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'PasteScript'
        # -*- Extra requirements: -*-
    ],
    test_suite='nose.collector',
    test_requires=['Nose', 'feedparser'],
    entry_points="""
    # -*- Entry points: -*-
    [paste.paster_create_template]
    mao_bao = mai.bao.package:Package
    """,
    )