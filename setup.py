from setuptools import setup, find_packages

version = '0.1'

setup(
    name='zohoapi',
    version=version,
    description="Python wrapper for Zoho API",
    long_description=open('README.rst').read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='zoho api',
    author='Rok Garbas',
    author_email='rok@garbas.si',
    url='https://github.com/collective/zohoapi',
    license='General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'simplejson',
        'poster',
        ],
    test_suite='zohoapi.tests.test_suite',
    )
