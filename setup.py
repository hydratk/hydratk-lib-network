# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import argv, version_info
from os import path, environ
from subprocess import call
from time import sleep
from pkgutil import find_loader
from platform import python_implementation
import hydratk.lib.install.task as task

with open("README.rst", "r") as f:
    readme = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]


def version_update(cfg, *args):

    major, minor = version_info[0], version_info[1]

    if (major == 2):
        cfg['modules'].append(
            {'module': 'jsonrpclib',   'version': '>=0.1.7',  'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'MySQL-python', 'version': '>=1.2.3',  'profile': 'db'})
        cfg['modules'].append(
            {'module': 'python-ldap',  'version': '>=2.4.25', 'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'scapy',        'version': '>=2.3.1',  'profile': 'basic'})
        if (minor == 6):
            cfg['modules'].append(
                {'module': 'simplejson', 'version': '==3.8.2', 'profile': 'basic'})
            cfg['modules'].append(
                {'module': 'stompest',   'version': '==2.1.6', 'profile': 'jms'})
        else:
            cfg['modules'].append(
                {'module': 'simplejson', 'version': '>=3.8.2', 'profile': 'basic'})
            cfg['modules'].append(
                {'module': 'stompest',   'version': '>=2.2.5', 'profile': 'jms'})
        cfg['modules'].append(
            {'module': 'suds',  'version': '>=0.4',   'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'tftpy', 'version': '>=0.6.2', 'profile': 'basic'})
    else:
        cfg['modules'].append(
            {'module': 'jsonrpclib-pelix', 'version': '>=0.2.8',   'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'mysqlclient',      'version': '>=1.3.7',   'profile': 'db'})
        cfg['modules'].append(
            {'module': 'pyldap',           'version': '>=2.4.25',  'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'scapy-python3',    'version': '>=0.18',    'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'simplejson',       'version': '>=3.8.2',   'profile': 'basic'})
        cfg['modules'].append(
            {'module': 'stompest',         'version': '>=2.2.5',   'profile': 'jms'})
        cfg['modules'].append(
            {'module': 'suds-py3',         'version': '>=1.3.2.0', 'profile': 'basic'})
        if (find_loader('tftpy') == None):
            cfg['modules'].append(
                {'module': 'git+https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy', 'profile': 'basic'})

        cfg['libs']['mysqlclient'] = cfg['libs']['MySQL-python']
        cfg['libs']['pyldap'] = cfg['libs']['python-ldap']

    if (python_implementation() != 'PyPy'):
        cfg['modules'].append(
            {'module': 'psycopg2', 'version': '>=2.4.5', 'profile': 'db'})
        cfg['modules'].append(
            {'module': 'pymssql',  'version': '>=2.1.3', 'profile': 'db'})
    else:
        cfg['modules'].append(
            {'module': 'psycopg2cffi', 'version': '>=2.7.4', 'profile': 'db'})
        cfg['modules'].append(
            {'module': 'git+https://github.com/dholth/pymssql.git', 'profile': 'db'})

        cfg['libs']['psycopg2cffi'] = cfg['libs']['psycopg2']
        cfg['libs'][
            'git+https://github.com/dholth/pymssql.git'] = cfg['libs']['pymssql']

    if ('ORACLE_HOME' not in environ):
        print (
            'Oracle has not been detected ($ORACLE_HOME is not set). If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
    else:
        if (python_implementation() != 'PyPy'):
            cfg['modules'].append(
                {'module': 'cx_Oracle', 'version': '>=5.1.3', 'profile': 'db'})
        else:
            cfg['modules'].append(
                {'module': 'git+https://github.com/lameiro/cx_oracle_on_ctypes.git', 'profile': 'db'})
            cfg['libs'][
                'git+https://github.com/lameiro/cx_oracle_on_ctypes.git'] = cfg['libs']['cx_Oracle']

    if (python_implementation() != 'PyPy'):
        if ('JAVA_HOME' not in environ):
            print (
                'Java has not been detected ($JAVA_HOME is not set). If you want to use HydraTK Java bridge, install Java first.')
            sleep(5)
        else:
            cfg['modules'].append(
                {'module': 'JPype1', 'version': '>=0.6.1', 'profile': 'bridge'})


def compile_java_classes(cfg, *args):

    dir = cfg['java']['dir']
    if (path.exists(dir)):
        classpath = cfg['java']['classpath']
        for file in cfg['java']['files']:
            print('Compiling {0}'.format(file))
            if (classpath != None):
                command = 'javac -cp {0} {1}'.format(classpath, file)
            else:
                command = 'javac {0}'.format(file)
            if (call(command, cwd=dir, shell=True) != 0):
                print('Failed to compile {0}'.format(file))

config = {
    'pre_tasks': [
        version_update,
        task.install_libs,
        task.install_modules
    ],

    'post_tasks': [
        task.copy_files,
        compile_java_classes
    ],

    'modules': [
        {'module': 'hydratk',
            'version': '>=0.4.0',    'profile': 'basic'},
        {'module': 'cassandra-driver',
                   'version': '>=3.7.0',    'profile': 'db'},
        {'module': 'lxml',
         'version': '>=3.3.3',    'profile': 'basic'},
        {'module': 'paho-mqtt',
            'version': '>=1.2',      'profile': 'jms'},
        {'module': 'paramiko',
            'version': '>=1.16.0',   'profile': 'basic'},
        {'module': 'pycurl',
            'version': '>=7.19.5.1', 'profile': 'basic'},
        {'module': 'pyexcel',
         'version': '>=0.2.0',    'profile': 'db'},
        {'module': 'pyexcel-xlsx',
         'version': '>=0.1.0',    'profile': 'db'},
        {'module': 'pyexcel-ods3',
            'version': '>=0.1.1',    'profile': 'db'},
        {'module': 'pymongo',
            'version': '>=3.3.0',    'profile': 'db'},
        {'module': 'python-qpid-proton',
         'version': '>=0.10',     'profile': 'jms'},
        {'module': 'pytz',
            'version': '>=2016.6.1', 'profile': 'basic'},
        {'module': 'redis',
            'version': '>=2.10.5',   'profile': 'db'},
        {'module': 'requests',
         'version': '>=2.11.1',   'profile': 'basic'},
        {'module': 'requests-ntlm',
            'version': '>=0.3.0',    'profile': 'basic'},
        {'module': 'selenium',
            'version': '>=2.46.1',   'profile': 'bridge'}
    ],

    'files': {
        'data': {
            'src/hydratk/lib/network/jms/java/JMSClient.java': '/var/local/hydratk/java',
            'src/hydratk/lib/network/jms/java/javaee.jar': '/var/local/hydratk/java',
            'src/hydratk/lib/network/dbi/java/DBClient.java': '/var/local/hydratk/java'
        }
    },

    'libs': {
        'cx_Oracle': {
            'apt-get': [
                'libaio1',
                'libaio-dev'
            ],
            'yum': [
                'libaio'
            ]
        },
        'lxml': {
            'repo': [
                'python-lxml'
            ],
            'apt-get': [
                'libxml2-dev',
                'libxslt1-dev'
            ],
            'yum': [
                'libxml2-devel',
                'libxslt-devel'
            ]
        },
        'MySQL-python': {
            'apt-get': [
                'python-mysqldb',
                'libmysqlclient-dev'
            ],
            'yum': [
                'mysql-devel'
            ]
        },
        'paramiko': {
            'apt-get': [
                'libffi-dev',
                'libssl-dev'
            ],
            'yum': [
                'libffi-devel',
                'openssl-devel'
            ]
        },
        'pymssql': {
            'apt-get': [
                'freetds-dev'
            ],
            'yum': [
                'freetds',
                'freetds-devel'
            ]
        },
        'psycopg2': {
            'repo': [
                'python-psycopg2'
            ],
            'apt-get': [
                'libpq-dev'
            ],
            'yum': [
                'postgresql-devel'
            ]
        },
        'pycurl': {
            'repo': [
                'python-pycurl'
            ],
            'apt-get': [
                'libcurl4-openssl-dev'
            ],
            'yum': [
                'libcurl-devel'
            ]
        },
        'python-ldap': {
            'apt-get': [
                'libldap2-dev',
                'libsasl2-dev',
                'libssl-dev'
            ],
            'yum': [
                'openldap-devel'
            ]
        },
        'selenium': {
            'apt-get': [
                'libfontconfig'
            ],
            'yum': [
                'fontconfig'
            ]
        }
    },

    'java': {
        'dir': '/var/local/hydratk/java',
        'files': [
            'DBClient.java',
            'JMSClient.java'
        ],
        'classpath': 'javaee.jar'
    }
}

task.run_pre_install(argv, config)

setup(
    name='hydratk-lib-network',
    version='0.2.1a.dev3',
    description='Clients/API for many network protocols and technologies',
    long_description=readme,
    author='Petr Rašek, HydraTK team',
    author_email='bowman@hydratk.org, team@hydratk.org',
    url='http://libraries.hydratk.org/network',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=classifiers,
    zip_safe=False,
    keywords='hydratk,database,soap,rest,jms,java,gui',
    requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
    platforms='Linux'
)

task.run_post_install(argv, config)
