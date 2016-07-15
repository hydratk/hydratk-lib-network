# -*- coding: utf-8 -*-

from subprocess import call, Popen, PIPE
from os import environ, path

def is_install_cmd(argv):

    res = False    
    if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
        res = True

    return res

def get_pck_manager():   
    
    pck_managers = ['apt-get', 'yum']
    
    pckm = []
    for pck in pck_managers:     
        if (is_installed(pck)):
            pckm.append(pck) 
    
    return pckm

def is_installed(app):      
    
    cmd = ['which', app]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate() 
    
    result = True if (len(out[0]) > 0) else False
    return result    

def install_pck(pckm, pck):  
    
    print('Installing package: {0}'.format(pck))
    
    if (pckm == 'apt-get'):
        cmd = 'apt-get -y install {0}'.format(pck)
    elif (pckm == 'yum'):
        cmd = 'yum -y install {0}'.format(pck)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to install package {0}'.format(pck)) 
        
def create_dir(dst):
    
    if (not path.exists(dst)):
        
        print('Creating directory {0}'.format(dst))
        cmd = 'mkdir -p {0}'.format(dst)
        
        if (call(cmd, shell=True) != 0):
            print('Failed to create directory {0}'.format(dst))     
        
def copy_file(src, dst):
    
    create_dir(dst)   
          
    print ('Copying file {0} to {1}'.format(src, dst))
    cmd = 'cp {0} {1}'.format(src, dst) 
    
    if (call(cmd, shell=True) != 0):
        print('Failed to copy {0} to {1}'.format(src, dst))         
        
def getenv(name):     
    
    value = environ[name] if (name in environ) else None
    return value                                                                    
        
def compile_java_class(dir, file, classpath=None):        
    
    print('Compiling {0}'.format(file))
    
    if (classpath != None):
        cmd = 'javac -cp {0} {1}'.format(classpath, file)
    else:
        cmd = 'javac {0}'.format(file)
        
    if (call(cmd, cwd=dir, shell=True) != 0):
        print('Failed to compile {0}'.format(file))         