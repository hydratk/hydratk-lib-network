.. _tutor_network_tut2_email:

Tutorial 2: Email
=================

This sections shows several examples how to use email client.

API
^^^

Module hydratk.lib.network.email.client.

Method EmailClient is factory method which requires attribute engine to create 
proper EmailClient object instance. Additional attributes are passed as args, kwargs. 

Supported protocols:

* SMTP/SMTPS: module smtp_client
* IMAP/IMAPS: module imap_client
* POP/POPS: module pop_client

  .. note::
      
     SMTPS initialization for versions Py3.4, Py3.5 can raise 
     starttls fails with tlsv1 alert decode error. The error is already reported.

Methods:

* connect: connect to mail server as sender (SMTP) or receiver (IMAP, POP)
* disconnect: disconnect from mail server
* send_email: send email (SMTP)
* email_count: count emails stored on server (IMAP, POP)
* list_emails: get list of emails stored on server (IMAP, POP)
* receive_email: receive email (IMAP, POP)

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

SMTP
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('smtp')
     
     # connect to SMTP server
     # returns bool
     client.connect(host='smtp.seznam.cz', user='lynushydra', passw='bowman')
     
     # send email
     subject = 'Hydra'
     message = 'This is testing email'
     sender = 'lynushydra@seznam.cz'
     recipients = ['lynushydra@seznam.cz']
     cc = ['lynus@gmail.com']
     bcc = ['lynus@gmail.com']
     
     # returns bool
     client.send_email(subject, message, recipients, cc, bcc) 
     
     # disconnect from server
     # returns bool
     client.disconnect()
     
  .. note::
   
     SMTPS client is initialized using constructor attribute secured=True.

IMAP
^^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('imap')
     
     # connect to IMAP server
     # returns bool
     client.connect(host='imap.seznam.cz', user='lynushydra', passw='bowman')
     
     # count emails
     count = client.email_count()
     
     # get email list
     # returns IDs
     emails = client.list_emails() 
     
     # receive email with ID 2
     sender, recipients, cc, subject, message = client.receive_email(2)
     
  .. note::
   
     IMAPS client is initialized using constructor attribute secured=True.     

POP
^^^  

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.email.client as email
    
     # initialize client
     client = email.EmailClient('imap')
     
     # connect to IMAP server
     # returns bool
     client.connect(host='pop3.seznam.cz', user='lynushydra', passw='bowman')
     
     # count emails
     count = client.email_count()
     
     # get email list
     # returns IDs
     emails = client.list_emails() 
     
     # receive email with ID 2
     sender, recipients, cc, subject, message = client.receive_email(2)
     
  .. note::
   
     POPS client is initialized using constructor attribute secured=True.     