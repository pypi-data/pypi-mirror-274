from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    include_package_data=True,
    name='ellis_django_views',
    version='0.1',
    packages=find_packages(),
    description='Generic views for Model View Serializer (MVS) pattern',
    author='Carl Victor Ellis',
    author_email='carl.ellis@hotmail.com.au',
    license='GNU',
    url='https://carlellis.io',
    long_description='Ellis views are generic views for Create, Request, Update and Delete views, simply define serializer_model, model and is_authorised methods.',
    long_description_content_type= 'text/x-rst',
    install_requires=[
        'django',
        'pillow',
        'djangorestframework',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)