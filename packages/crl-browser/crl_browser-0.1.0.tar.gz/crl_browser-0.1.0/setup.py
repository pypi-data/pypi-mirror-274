from setuptools import setup, find_packages

setup(
    name='crl-browser',
    version='0.1.0',
    author='Goychay__23',
    author_email='goychaylii23@gmail.com',
    description='crl net browsering',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Goychay23/crlbrowsering',
    packages=find_packages('crl-browser.py'),
    license='LGPL-3.0-or-later',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[
        'requests',
        'psycopg2',
        'PyQt6',
    ],
)
