# -*- coding: utf-8 -*-

from setuptools import setup as st_setup
from setuptools import find_packages as st_find_packages
from sys import argv, version_info
from os import path, environ
from subprocess import call
from time import sleep
from pkgutil import find_loader
from platform import python_implementation
import hydratk.lib.install.task as task
import hydratk.lib.system.config as syscfg

try:
    os_info = syscfg.get_supported_os()
except Exception as exc:
    print(str(exc))
    exit(1)

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
        cfg['modules'].append({'module': 'jsonrpclib', 'version': '>=0.1.7', 'profile': 'basic'})
        cfg['modules'].append({'module': 'MySQL-python', 'version': '>=1.2.3', 'profile': 'db'})
        cfg['modules'].append({'module': 'python-ldap', 'version': '>=2.4.25', 'profile': 'db'})
        cfg['modules'].append({'module': 'scapy', 'version': '>=2.3.1', 'profile': 'basic'})
        if (minor == 6):
            cfg['modules'].append({'module': 'simplejson', 'version': '==3.8.2', 'profile': 'basic'})
            cfg['modules'].append({'module': 'stompest', 'version': '==2.1.6', 'profile': 'jms'})
        else:
            cfg['modules'].append({'module': 'simplejson', 'version': '>=3.8.2', 'profile': 'basic'})
            cfg['modules'].append({'module': 'stompest', 'version': '>=2.2.5', 'profile': 'jms'})
        cfg['modules'].append({'module': 'suds', 'version': '>=0.4', 'profile': 'basic'})
        cfg['modules'].append({'module': 'tftpy', 'version': '>=0.6.2', 'profile': 'basic'})
    else:
        cfg['modules'].append({'module': 'jsonrpclib-pelix', 'version': '>=0.2.8', 'profile': 'basic'})
        cfg['modules'].append({'module': 'mysqlclient', 'version': '>=1.3.7', 'profile': 'db'})
        cfg['modules'].append({'module': 'pyldap', 'version': '>=2.4.25', 'profile': 'db'})
        cfg['modules'].append({'module': 'scapy-python3', 'version': '>=0.18', 'profile': 'basic'})
        cfg['modules'].append({'module': 'simplejson', 'version': '>=3.8.2', 'profile': 'basic'})
        cfg['modules'].append({'module': 'stompest', 'version': '>=2.2.5', 'profile': 'jms'})
        cfg['modules'].append({'module': 'suds-py3', 'version': '>=1.3.2.0', 'profile': 'basic'})
        if (find_loader('tftpy') == None):
            cfg['modules'].append({'module': 'git+https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy', 'profile': 'basic'})

        cfg['libs']['lxml']['freebsd']['pkg'] = ['py36-lxml']
        cfg['libs']['mysqlclient'] = cfg['libs']['MySQL-python']
        cfg['libs']['mysqlclient']['freebsd']['pkg'] = ['py36-mysqlclient']
        cfg['libs']['psycopg2']['freebsd']['pkg'] = ['py36-psycopg2']
        cfg['libs']['pyldap'] = cfg['libs']['python-ldap']

    if (os_info['compat'] != 'arch'):
        cfg['modules'].append({'module': 'python-qpid-proton', 'version': '>=0.10', 'profile': 'jms'})

    if (python_implementation() != 'PyPy'):
        cfg['modules'].append({'module': 'psycopg2', 'version': '>=2.4.5', 'profile': 'db'})
        if (os_info['compat'] not in ['slackware', 'freebsd']):
            cfg['modules'].append({'module': 'pymssql', 'version': '>=2.1.3', 'profile': 'db'})
    else:
        cfg['modules'].append({'module': 'psycopg2cffi', 'version': '>=2.7.4', 'profile': 'db'})
        cfg['libs']['psycopg2cffi'] = cfg['libs']['psycopg2']

    if ('ORACLE_HOME' not in environ):
        print ('Oracle has not been detected ($ORACLE_HOME is not set). If you want to use HydraTK Oracle client, install Oracle first.')
        sleep(5)
    else:
        if (python_implementation() != 'PyPy'):
            cfg['modules'].append({'module': 'cx_Oracle', 'version': '>=5.1.3', 'profile': 'db'})
        elif (find_loader('cx_Oracle') == None):
            cfg['modules'].append({'module': 'git+https://github.com/lameiro/cx_oracle_on_ctypes.git', 'profile': 'db'})
            cfg['libs']['git+https://github.com/lameiro/cx_oracle_on_ctypes.git'] = cfg['libs']['cx_Oracle']

    if (python_implementation() != 'PyPy'):
        if ('JAVA_HOME' not in environ):
            print ('Java has not been detected ($JAVA_HOME is not set). If you want to use HydraTK Java bridge, install Java first.')
            del cfg['post_tasks'][1]
            sleep(5)
        else:
            cfg['modules'].append({'module': 'JPype1', 'version': '>=0.6.1', 'profile': 'bridge'})

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
        {'module': 'hydratk', 'version': '>=0.5.0', 'profile': 'basic'},
        {'module': 'cassandra-driver', 'version': '>=3.7.0', 'profile': 'db'},
        {'module': 'imageio', 'version': '>=2.3.0', 'profile': 'bridge'},
        {'module': 'lxml', 'version': '>=3.3.3', 'profile': 'basic'},
        {'module': 'paho-mqtt', 'version': '>=1.2', 'profile': 'jms'},
        {'module': 'paramiko', 'version': '>=1.16.0', 'profile': 'basic'},
        {'module': 'pycurl', 'version': '>=7.19.5.1', 'profile': 'basic'},
        {'module': 'pyexcel', 'version': '>=0.2.0', 'profile': 'db'},
        {'module': 'pyexcel-xlsx', 'version': '>=0.1.0', 'profile': 'db'},
        {'module': 'pyexcel-ods3', 'version': '>=0.1.1', 'profile': 'db'},
        {'module': 'pymongo', 'version': '>=3.3.0', 'profile': 'db'},
        {'module': 'pytz', 'version': '>=2016.6.1', 'profile': 'basic'},
        {'module': 'redis', 'version': '>=2.10.5', 'profile': 'db'},
        {'module': 'requests', 'version': '>=2.11.1', 'profile': 'basic'},
        {'module': 'requests-ntlm', 'version': '>=0.3.0', 'profile': 'basic'},
        {'module': 'selenium', 'version': '>=2.46.1', 'profile': 'bridge'}
    ],

    'files': {
        'data': {
            'src/hydratk/lib/network/jms/java/JMSClient.java': '{0}/hydratk/java'.format(syscfg.HTK_VAR_DIR),
            'src/hydratk/lib/network/jms/java/javaee.jar': '{0}/hydratk/java'.format(syscfg.HTK_VAR_DIR),
            'src/hydratk/lib/network/dbi/java/DBClient.java': '{0}/hydratk/java'.format(syscfg.HTK_VAR_DIR)
        }
    },

    'libs': {
        'cx_Oracle': {
            'debian': {
                'apt-get': [
                    'libaio1',
                    'libaio-dev'
                ],
                'check': {
                    'libaio1': {
                        'cmd': '/sbin/ldconfig -p | grep libaio || locate -b libaio | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libaio'
                    },
                    'libaio-dev': {
                        'cmd': 'dpkg --get-selections | grep libaio-dev || locate -b libaio-dev | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libaio-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'libaio'
                ],
                'check': {
                    'libaio': {
                        'cmd': '/sbin/ldconfig -p | grep libaio || locate -b libaio | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libaio'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'libaio'
                ],
                'check': {
                    'libaio': {
                        'cmd': '/sbin/ldconfig -p | grep libaio || locate -b libaio | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libaio'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'libaio1'
                ],
                'check': {
                    'libaio1': {
                        'cmd': '/sbin/ldconfig -p | grep libaio || locate -b libaio | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libaio1'
                    }
                }
            }
        },
        'imageio': {
            'debian': {
                'apt-get': [
                    'libjpeg-dev',
                    'zlib1g-dev'
                ],
                'check': {
                    'libjpeg-dev': {
                        'cmd': 'dpkg --get-selections | grep libjpeg-dev || locate -b libjpeg | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libjpeg-dev'
                    },
                    'zlib1g-dev': {
                        'cmd': 'dpkg --get-selections | grep zlib1g-dev || locate -b zlib | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package zlib1g-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'libjpeg-devel',
                    'zlib-devel'
                ],
                'check': {
                    'libjpeg-dev': {
                        'cmd': 'yum list installed | grep libjpeg-turbo-devel || locate -b libjpeg | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libjpeg-devel'
                    },
                    'zlib1g-dev': {
                        'cmd': 'yum list installed | grep zlib-devel || locate -b zlib | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package zlib-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'libjpeg-devel',
                    'zlib-devel'
                ],
                'check': {
                    'libjpeg-dev': {
                        'cmd': 'dnf list installed | grep libjpeg || locate -b libjpeg | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libjpeg-devel'
                    },
                    'zlib1g-dev': {
                        'cmd': 'dnf list installed | grep zlib-devel || locate -b zlib | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package zlib-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'libjpeg-devel',
                    'zlib-devel'
                ],
                'check': {
                    'libjpeg-dev': {
                        'cmd': 'dnf list installed | grep libjpeg || locate -b libjpeg | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libjpeg-devel'
                    },
                    'zlib1g-dev': {
                        'cmd': 'dnf list installed | grep zlib-devel || locate -b zlib | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package zlib-devel'
                    }
                }
            }
        },
        'lxml': {
            'debian': {
                'apt-get': [
                    'python-lxml',
                    'libxml2-dev',
                    'libxslt1-dev'                    
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'dpkg --get-selections | grep python-lxml || locate -b lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-dev': {
                        'cmd': 'dpkg --get-selections | grep libxml2-dev || locate -b libxml2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libxml2-dev'
                    },
                    'libxslt1-dev': {
                        'cmd': 'dpkg --get-selections | grep libxslt1-dev || locate -b libxslt | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libxslt1-dev'
                    }                          
                }
            },
            'redhat': {
                'yum': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'yum list installed | grep python-lxml || locate -b lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'yum list installed | grep libxml2-devel || locate -b libxml2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'yum list installed | grep libxslt-devel || locate -b libxslt | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'dnf list installed | grep python-lxml || locate -b lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'dnf list installed | grep libxml2-devel || locate -b libxml2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'dnf list installed | grep libxslt-devel || locate -b libxslt | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'python-lxml',
                    'libxml2-devel',
                    'libxslt-devel'
                ],
                'check': {
                    'python-lxml': {
                        'cmd': 'rpm -qa | grep python-lxml || locate -b lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package python-lxml'
                    },
                    'libxml2-devel': {
                        'cmd': 'rpm -qa | grep libxml2-devel || locate -b libxml2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libxml2-devel'
                    },
                    'libxslt-devel': {
                        'cmd': 'rpm -qa | grep libxslt-devel || locate -b libxslt | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate shared library libxslt-devel'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'py27-lxml'
                ],
                'check': {
                    'py27-lxml': {
                        'cmd': 'pkg info | grep py27-lxml || locate lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py27-lxml'
                    },
                    'py36-lxml': {
                        'cmd': 'pkg info | grep py36-lxml || locate lxml | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py36-lxml'
                    }
                }
            }
        },
        'MySQL-python': {
            'debian': {
                'apt-get': [
                    'libmysqlclient-dev'                            
                ],
                'check': {
                    'libmysqlclient-dev': {
                        'cmd': 'dpkg --get-selections | grep libmysqlclient-dev || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libmysqlclient-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'mysql-devel'
                ],
                'check': {
                    'mysql-devel': {
                        'cmd': 'yum list installed | grep mariadb-devel || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package mariadb-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'mysql-devel'
                ],
                'check': {
                    'mysql-devel': {
                        'cmd': 'dnf list installed | grep mariadb-devel || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package mariadb-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'libmysqlclient-devel'
                ],
                'check': {
                    'libmysqlclient-devel': {
                        'cmd': 'rpm -qa | grep libmysqlclient-devel || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libmysqlclient-devel'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'mysqlclient'
                ],
                'check': {
                    'mysqlclient': {
                        'cmd': 'ls -d /var/db/pkg/*/* | grep mysqlclient || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package mysqlclient'
                    }
                }
            },
            'arch': {
                'pacman': [
                    'mysql-python'
                ],
                'check': {
                    'mysql-python': {
                        'cmd': 'pacman -Q mysql-python || locate -b libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package mysql-python'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'py27-MySQLdb'
                ],
                'check': {
                    'py27-MySQLdb': {
                        'cmd': 'pkg info | grep py27-MySQLdb || locate libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py27-MySQLdb'
                    },
                    'py36-mysqlclient': {
                        'cmd': 'pkg info | grep py36-mysqlclient || locate libmysqlclient | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py36-mysqlclient'
                    }                        
                }
            }
        },
        'paramiko': {
            'debian': {
                'apt-get': [
                    'libffi-dev',
                    'libssl-dev'
                ],
                'check': {
                   'libffi-dev': {
                        'cmd': 'dpkg --get-selections | grep libffi-dev || locate -b libffi | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libffi-dev'
                    },
                   'libssl-dev': {
                        'cmd': 'dpkg --get-selections | grep libssl-dev || locate -b libssl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libssl-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'libffi-devel',
                    'openssl-devel'
                ],
                'check': {
                   'libffi-devel': {
                        'cmd': 'yum list installed | grep libffi-devel || locate -b libffi | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libffi-devel'
                    },
                   'openssl-devel': {
                        'cmd': 'yum list installed | grep openssl-devel || locate -b libssl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openssl-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'libffi-devel',
                    'openssl-devel'
                ],
                'check': {
                   'libffi-devel': {
                        'cmd': 'dnf list installed | grep libffi-devel || locate -b libffi | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libffi-devel'
                    },
                   'openssl-devel': {
                        'cmd': 'dnf list installed | grep openssl-devel || locate -b libssl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openssl-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'libffi-devel'
                ],
                'check': {
                   'libffi-devel': {
                        'cmd': 'rpm -qa | grep libffi-devel || locate -b libffi | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libffi-devel'
                    }
                }
            }
        },
        'psycopg2': {
            'debian': {
                'apt-get': [
                    'libpq-dev'
                ],
                'check': {
                   'libpq-dev': {
                        'cmd': 'dpkg --get-selections | grep libpq-dev || locate -b libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libpq-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'postgresql-devel'
                ],
                'check': {
                   'postgresql-devel': {
                        'cmd': 'yum list installed | grep postgresql-devel || locate -b libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package postgresql-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'postgresql-devel'
                ],
                'check': {
                   'postgresql-devel': {
                        'cmd': 'dnf list installed | grep postgresql-devel || locate libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package postgresql-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'postgresql-devel'
                ],
                'check': {
                   'postgresql-devel': {
                        'cmd': 'rpm -qa | grep postgresql-devel || locate libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package postgresql-devel'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'py27-psycopg2'
                ],
                'check': {
                   'py27-psycopg2': {
                        'cmd': 'pkg info | grep py27-psycopg2 || locate libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py27-psycopg2'
                    },
                   'py36-psycopg2': {
                        'cmd': 'pkg info | grep py36-psycopg2 || locate libpq | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package py36-psycopg2'
                    }
                }
            }                     
        },
        'pycurl': {
            'debian': {
                'apt-get': [
                    'libcurl4-openssl-dev'
                ],
                'check': {
                   'libcurl4-openssl-dev': {
                        'cmd': 'dpkg --get-selections | grep libcurl4-openssl-dev || locate -b libcurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libcurl4-openssl-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'libcurl-devel'
                ],
                'check': {
                   'libcurl-devel': {
                        'cmd': 'yum list installed | grep libcurl-devel || locate -b libcurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libcurl-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'libcurl-devel'
                ],
                'check': {
                   'libcurl-devel': {
                        'cmd': 'dnf list installed | grep libcurl-devel || locate -b libcurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libcurl-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'libcurl-devel'
                ],
                'check': {
                   'libcurl-devel': {
                        'cmd': 'rpm -qa | grep libcurl-devel || locate -b libcurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libcurl-devel'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'pycurl'
                ],
                'check': {
                   'pycurl': {
                        'cmd': 'ls -d /var/db/pkg/*/* | grep pycurl || locate -b pycurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package pycurl'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'curl'
                ],
                'check': {
                   'curl': {
                        'cmd': 'pkg info | grep curl || locate libcurl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package curl'
                    }
                }
            }                   
        },
        'pymssql': {
            'debian': {
                'apt-get': [
                    'freetds-dev'
                ],
                'check': {
                   'freetds-dev': {
                        'cmd': 'dpkg --get-selections | grep freetds-dev || locate -b freetds-dev | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'freetds',
                    'freetds-devel'
                ],
                'check': {
                   'freetds': {
                        'cmd': 'yum list installed | grep freetds || locate -b freetds | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds'
                    },
                   'freetds-devel': {
                        'cmd': 'yum list installed | grep freetds-devel || locate -b freetds-devel | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'freetds',
                    'freetds-devel'
                ],
                'check': {
                   'freetds': {
                        'cmd': 'dnf list installed | grep freetds || locate -b freetds | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds'
                    },
                   'freetds-devel': {
                        'cmd': 'dnf list installed | grep freetds-devel || locate -b freetds-devel | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'freetds',
                    'freetds-devel'
                ],
                'check': {
                   'freetds': {
                        'cmd': 'rpm -qa | grep freetds || locate -b freetds | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds'
                    },
                   'freetds-devel': {
                        'cmd': 'rpm -qa | grep freetds-devel || locate -b freetds | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package freetds-devel'
                    }
                }
            }
        },
        'python-ldap': {
            'debian': {
                'apt-get': [
                    'libldap2-dev',
                    'libsasl2-dev',
                    'libssl-dev'
                ],
                'check': {
                   'libldap2-dev': {
                        'cmd': 'dpkg --get-selections | grep libldap2-dev || locate -b libldap | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libldap2-dev'
                    },
                   'libsasl2-dev': {
                        'cmd': 'dpkg --get-selections | grep libsasl2-dev || locate -b libsasl2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libsasl2-dev'
                    },
                   'libssl-dev': {
                        'cmd': 'dpkg --get-selections | grep libssl-dev || locate -b libssl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libssl-dev'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'openldap-devel'
                ],
                'check': {
                   'openldap-devel': {
                        'cmd': 'yum list installed | grep openldap-devel || locate -b libldap | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openldap-devel'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'openldap-devel'
                ],
                'check': {
                   'openldap-devel': {
                        'cmd': 'dnf list installed | grep openldap-devel || locate -b libldap | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openldap-devel'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'openldap2-devel'
                ],
                'check': {
                   'openldap2-devel': {
                        'cmd': 'rpm -qa | grep openldap2-devel || locate -b libldap | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openldap2-devel'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'openldap',
                    'cyrus-sasl'
                ],
                'check': {
                   'openldap': {
                        'cmd': 'ls -d /var/db/pkg/*/* | grep openldap || locate -b libldap | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openldap'
                    },
                   'cyrus-sasl': {
                        'cmd': 'ls -d /var/db/pkg/*/* | grep cyrus-sasl || locate -b cyrus-sasl | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package cyrus-sasl'
                    }
                }
            },
            'freebsd': {
                'pkg': [
                    'openldap-sasl-client'
                ],
                'check': {
                   'openldap-sasl-client': {
                        'cmd': 'pkg info | grep openldap-sasl-client || locate libsasl2 | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package openldap-sasl-client'
                    }
                }
            }
        },
        'selenium': {
            'debian': {
                'apt-get': [
                    'libfontconfig'
                ],
                'check': {
                   'libfontconfig': {
                        'cmd': 'dpkg --get-selections | grep libfontconfig || locate -b libfontconfig | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package libfontconfig'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'fontconfig'
                ],
                'check': {
                   'fontconfig': {
                        'cmd': 'yum list installed | grep fontconfig || locate -b libfontconfig | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package fontconfig'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'fontconfig'
                ],
                'check': {
                   'fontconfig': {
                        'cmd': 'dnf list installed | grep fontconfig || locate -b libfontconfig | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package fontconfig'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'fontconfig'
                ],
                'check': {
                   'fontconfig': {
                        'cmd': 'rpm -qa | grep fontconfig || locate -b libfontconfig | grep {0}'.format(syscfg.HTK_ROOT_DIR),
                        'errmsg': 'Unable to locate package fontconfig'
                    }
                }
            }                     
        },
        'git+https://github.com/ZuljinSBK/tftpy.git@master#egg=tftpy': {
            'debian': {
                'apt-get': [
                    'git'
                ],
                'check': {
                    'git': {
                        'cmd': 'which git',
                        'errmsg': 'Required git not found'
                    }
                }
            },
            'redhat': {
                'yum': [
                    'git'
                ],
                'check': {
                    'git': {
                        'cmd': 'which git',
                        'errmsg': 'Required git not found'
                    }
                }
            },
            'fedora': {
                'dnf': [
                    'git'
                ],
                'check': {
                    'git': {
                        'cmd': 'which git',
                        'errmsg': 'Required git not found'
                    }
                }
            },
            'suse': {
                'zypper': [
                    'git'
                ],
                'check': {
                    'git': {
                        'cmd': 'which git',
                        'errmsg': 'Required git not found'
                    }
                }
            },
            'gentoo': {
                'emerge': [
                    'dev-vcs/git'
                ],
                'check': {
                    'dev-vcs/git': {
                        'cmd': 'which git',
                        'errmsg': 'Required git not found'
                    }
                }
            }
        }
    },

    'java': {
        'dir': '{0}/hydratk/java'.format(syscfg.HTK_VAR_DIR),
        'files': [
            'DBClient.java',
            'JMSClient.java'
        ],
        'classpath': 'javaee.jar'
    }
}

task.run_pre_install(argv, config)

st_setup(
    name='hydratk-lib-network',
    version='0.2.3',
    description='Clients/API for many network protocols and technologies',
    long_description=readme,
    author='Petr Rašek, HydraTK team',
    author_email='bowman@hydratk.org, team@hydratk.org',
    url='http://libraries.hydratk.org/network',
    license='BSD',
    packages=st_find_packages('src'),
    package_dir={'': 'src'},
    classifiers=classifiers,
    zip_safe=False,
    keywords='hydratk,database,soap,rest,jms,java,gui',
    requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
    platforms='Linux,FreeBSD'
)

task.run_post_install(argv, config)
