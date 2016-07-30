# -*- coding: utf-8 -*-
"""Bridge to Java virtual machine

.. module:: bridge.java
   :platform: Unix
   :synopsis: Bridge to Java virtual machine
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
java_before_start
java_after_start
java_before_stop
java_after_stop

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from jpype import JByte, JShort, JInt, JLong, JFloat, JDouble, JChar, JString, JBoolean
from jpype import get_default_jvm_path, isJVMStarted, startJVM, shutdownJVM, JavaException
from jpype import JClass, JPackage
from os import path, walk

java_types = {
  'byte'  : JByte,
  'short' : JShort,
  'int'   : JInt,
  'long'  : JLong,
  'float' : JFloat,
  'double': JDouble,
  'char'  : JChar,
  'string': JString,
  'bool'  : JBoolean
}

class JavaBridge(object):
    """Class JavaBridge
    """

    _mh = None
    _jvm_path = None
    _classpath = None
    _status = None
    
    def __init__(self, jvm_path=None, classpath=None):
        """Class constructor
           
        Called when the object is initialized
        
        Args:                   
           jvm_path (str): JVM location, default from configuration
           classpath (str): Java classpath, default from configuration
           
        """         
        
        self._mh = MasterHead.get_head()  
        self._mh.find_module('hydratk.lib.bridge.java', None)        
        
        if (jvm_path != None):
            self._jvm_path = jvm_path
        else: 
            cfg = self._mh.cfg['Libraries']['hydratk.lib.bridge.java']['jvm_path']
            self._jvm_path = cfg if (cfg != 'default') else get_default_jvm_path()
             
        self._classpath = self._set_classpath(classpath)   
        
    @property
    def jvm_path(self):
        """ JVM path property getter """
        
        return self._jvm_path
    
    @property
    def classpath(self):
        """ JVM classpath property getter """
        
        return self._classpath
    
    @property
    def status(self):
        """ JVM status property getter """
        
        return self._status                                                        
        
    def start(self, options=[]):
        """Method starts JVM 
        
        Args:
           options (list): JVM options

        Returns:
           bool: result
           
        Raises:
           event: java_before_start
           event: java_after_start
                
        """          
        
        try:
            
            if (self._status):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_already_started'), self._mh.fromhere())
                return True
            elif (isJVMStarted()):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_java_restart_tried'), self._mh.fromhere())
                return False
                                                      
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_starting_jvm', self._jvm_path,
                          self.classpath, options), self._mh.fromhere())
                
            ev = event.Event('java_before_start', options)
            if (self._mh.fire_event(ev) > 0):
                options = ev.argv(0)                
                
            if (ev.will_run_default()):                  
                if (self._classpath != None):
                    options.append('-Djava.class.path={0}'.format(self._classpath))
                
                startJVM(self._jvm_path, *options)
                    
                self._status = True
                result = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_started'), self._mh.fromhere()) 
            ev = event.Event('java_after_start')
            self._mh.fire_event(ev)                  
                
            return result
            
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None         
    
    def stop(self):
        """Method stops JVM
        
        Args:
           none
            
        Returns:
           bool: result
           
        Raises:
           event: java_before_stop
           event: java_after_stop        
                
        """          
        
        try:
            
            if (not self._status):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_java_not_started'), self._mh.fromhere())
                return False                
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_stopping_jvm'), self._mh.fromhere())
            ev = event.Event('java_before_stop')
            self._mh.fire_event(ev)
                        
            shutdownJVM()
            self._status = False
            result = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_stopped'), self._mh.fromhere()) 
            ev = event.Event('java_after_stop')
            self._mh.fire_event(ev)                
                
            return result
          
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None         
    
    def get_var(self, datatype, value):
        """Method creates Java variable
        
        Args:
           datatype (str): byte|short|int|long|float|double|char|string|bool
           value (str): initial value
            
        Returns:
           obj: Java variable
                
        """          
        
        try:
        
            if (datatype not in java_types):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_java_unknown_type', datatype), self._mh.fromhere())
                return None        
            else: 
                return java_types[datatype](value)
            
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None            
        
    def get_class(self, name, *attrs):
        """Method creates Java class instance
        
        Args:
           name (str): class name
           attrs (args): constructor attributes
            
        Returns:
           obj: class instance
                
        """          
        
        try:

            return JClass(name)(*attrs)
        
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None    
        
    def desc_class(self, name):
        """Method describes Java class
        
        Args:
           name (str): class name
            
        Returns:
           tuple: attribute names, method names
                
        """         
        
        try:
            
            attrs = []
            methods = []
            
            for name, type in JClass(name).__dict__.items():
                if (type.__class__.__name__ == 'property'):
                    attrs.append(name)
                elif (type.__class__.__name__ == 'JavaMethod'):
                    methods.append(name)
            
            return attrs, methods
        
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None   
        
    def get_package(self, name):
        """Method returns package
        
        Args:
           name (str): package name
            
        Returns:
           obj: method
                
        """  
                
        try:

            package = JPackage(name)
            return package
        
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None             
        
    def init_arraylist(self, array):
        """Method initializes Java ArrayList
        
        Args:
           list (list): Python list
            
        Returns:
           obj: Java ArrayList
                
        """          
        
        try:
            
            arraylist = self.get_class('java.util.ArrayList')
            for value in array:
                arraylist.add(str(value))  
                
            return arraylist 
        
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None           
          
        
    def init_hashmap(self, dictionary):
        """Method initializes Java HashMap
        
        Args:
           dictionary (dict): Python dictionary
            
        Returns:
           obj: Java HashMap
                
        """          
        
        try:
            
            hashmap = self.get_class('java.util.concurrent.ConcurrentHashMap')
            for key, value in dictionary.items():
                hashmap.put(str(key), str(value))   
                
            return hashmap 
        
        except (RuntimeError, JavaException) as ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None   
        
    def _set_classpath(self, classpath=None):
        """Method sets classpath
        
        Args:
           classpath (str): path to be appended to configured classpath

        Returns:
           str: classpath
                
        """          
        
        cfg = self._mh.cfg['Libraries']['hydratk.lib.bridge.java']['classpath']
        if (classpath != None):
            cfg += ':' + classpath
          
        exp_classpath = ''             
        for entry in cfg.split(':'):
            
            if (path.isfile(entry)):
                exp_classpath += entry + ':'
            else:
                                
                for dirname, _, filelist in walk(entry):   
                    exp_classpath += dirname + ':'    
                    for filename in filelist:
                        if (filename.split('.')[-1] == 'jar'):
                            exp_classpath += path.join(dirname, filename) + ':'
                            
        return exp_classpath[:-1]                                         