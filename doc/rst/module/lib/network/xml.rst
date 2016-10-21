.. _module_lib_data_xml:

XML
===

This sections contains module documentation of xml module.

xml
^^^

Module loader provides class XMLValidate for data validation according to XSD using external module lxml.
Unit tests available at hydratk/lib/data/xml/01_methods_ut.jedi

**Attributes** :

_xml_schema - parsed xsd file

**Methods** :

* xsd_validate_file

Method loads xml file and validates the content according to xsd using method xsd_validate.

* xsd_validate

Method transforms xml string to lxml.etree and validates it according to xsd. 
It raises error if xml is invalid (DocumentInvalid, XMLSyntaxError).

* load_xsd_file

Method loads xsd file and sets _xml_schema using method load_xsd.

* load_xsd

Method transforms xsd string to lxml.etree.XMLSchema and sets _xml_schema.

  .. code-block:: python
  
     # load xsd file
     c = XMLValidate()
     path = '/var/local/hydratk/testenv/crm.xsd'
     c.load_xsd_file(path)
     
     # validate xml file according to xsd       
     path = '/var/local/hydratk/test.xml'               
     c.xsd_validate_file(path)  