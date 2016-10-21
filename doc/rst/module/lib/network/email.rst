.. _module_lib_network_email:

EMAIL
=====

This sections contains module documentation of email module.

client
^^^^^^

Module client provides common way to initialize email client.
It implements factory design pattern, each client provides class EmailClient.
Unit tests available at hydratk/lib/network/email/client/01_methods_ut.jedi

Following **protocols** are supported:

* SMTP - module smtp_client
* POP - module pop_client
* IMAP - module imap_client

**Methods** :

* EmailClient 

Creates EmailClient instance of given protocol (use protocol name, case is ignored).
Any constructor parameters can be passed as args, kwargs. When engine is not supported NotImplementedError is raised.

  .. code-block:: python
  
     from hydratk.lib.network.email.client import EmailClient
     
     c1 = EmailClient('SMTP')
     c2 = EmailClient('POP', secured=True, verbose=True)
     
smtp_client
^^^^^^^^^^^

Module provides class EmailClient which implements SMTP client using Python module 
`smtplib <https://docs.python.org/3.6/library/smtplib.html>`_.
Unit tests available at hydratk/lib/network/email/smtp_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - smtplib client instance
* _secured - bool, secured protocol SMTPS
* _host - server hostname (or IP address)
* _port - port number (default 25 for SMTP, 465 for SMTPS)
* _user - username
* _passw - password
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* secured - returns _secured
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Constructor called by EmailClient method. Sets _client to smtplib client instance (using constructor SMTP or SMTP_SSL depending on _secured).
Turns verbose mode if enabled (smtplib method set_debuglevel), not secured protocol is used by default.

* connect

Connects to email server (specified via parameters host, port, user, passw).
First fires event email_before_connect where parameters can be rewritten. Connects to server using method smtplib method connect and login.
After successful connection fires event email_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.email.client import EmailClient
     
     c = EmailClient('SMTP')
     res = c.connect(host='smtp.seznam.cz', port=25, user='hydra', passw='hydra')     

* disconnect

Disconnects from database using smtplib method quit and returns bool.

  .. code-block:: python
  
     res = c.disconnect()
      
* send_email

Sends email to server. First fires event email_before_send_email where parameters (subject, message, sender, recipients, cc, bcc) can be rewritten.
recipients, cc, bcc are list parameters. sender should be email you are authorized to use, otherwise email server would reject the attempt.
recipients mustn't be existing addresses, if not email server delivers error email. Prepares email body in form 

From: sender 
To: recipients 
CC: cc 
Subject: subject 
message

and sends it using smtplib method sendmail. BCC is hidden so it isn't stored in body.
After that method fires event email_after_send_email and returns bool.

  .. code-block:: python
  
     # single recipient
     subject, message, sender, recipients = 'test', 'test msg', 'hydra@seznam.cz', ['hydra@hydratk.org']  
     res = c.send_email(subject, message, sender, recipients)      
     
     # multiple recipients and copy
     recipients, cc = ['hydra@hydratk.org', 'hydratk@hydratk.org'], [hydra2@hydratk.org]      
     res = c.send_email(subject, message, sender, recipients, cc)    
     
pop_client
^^^^^^^^^^

Module provides class EmailClient which implements POP client using Python module 
`poplib <https://docs.python.org/3.6/library/poplib.html>`_.
Unit tests available at hydratk/lib/network/email/pop_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - poplib client instance
* _secured - bool, secured protocol POPS
* _host - server hostname (or IP address)
* _port - port number (default 110 for POP, 995 for POPS)
* _user - username
* _passw - password
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* secured - returns _secured
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Sets MasterHead reference and stores _verbose, _secured parameters.

* connect

Connects to email server (specified via parameters host, port, user, passw). First fires event email_before_connect where parameters can be 
rewritten. Sets _client to poplib client instance (using constructor POP or POP_SSL depending on _secured) and connects to server 
(authentication using poplib method user, pass). Turns verbose mode if enabled (poplib method set_debuglevel), not secured protocol is used by default.
After successful connection fires event email_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.email.client import EmailClient
     
     c = EmailClient('POP')
     res = c.connect(host='pop3.seznam.cz', port=110, user='hydra', passw='hydra')     

* disconnect

Disconnects from database using poplib method quit and returns bool.

  .. code-block:: python
  
     res = c.disconnect()     
     
* email_count

Counts emails in mailbox on server using poplib method stat. Returns count.

  .. code-block:: python
  
     res = c.email_count()       
     
* list_emails

Lists email in mailbox on server using poplib method list. Returns list of email ids.

  .. code-block:: python
  
     res = c.list_emails()     
     
* receive_email

Receives given email from server. First fires event email_before_receive_email where parameter msg_id can be rewritten.
Downloads email using poplib method retr and parses it. 

From: sender
To: recipient1,recipient2,...
CC: cc1,cc2,...
Subject: subject
Inbound message
message

After that method fires event email_after_receive_email and returns tuple (sender, recipients, cc, subject, message).

  .. code-block:: python
  
     # first email
     res = c.receive_email(1)
     
     # last email
     res = c.receive_email(c.email_count())       
     
imap_client
^^^^^^^^^^^

Module provides class EmailClient which implements IMAP client using Python module 
`imaplib <https://docs.python.org/3.6/library/imaplib.html>`_.
Unit tests available at hydratk/lib/network/email/imap_client/01_methods_ut.jedi

**Attributes** :

* _mh - MasterHead reference
* _client - imaplib client instance
* _secured - bool, secured protocol IMAPS
* _host - server hostname (or IP address)
* _port - port number (default 143 for IMAP, 993 for IMAPS)
* _user - username
* _passw - password
* _verbose - bool, verbose mode
* _is_connected - bool, set to True/False after successful connect/disconnect. Some methods are disabled if not connected.

**Properties (Getters)** :

* client - returns _client
* secured - returns _secured
* host - returns _host
* port - returns _port
* user - returns _user
* passw - returns _passw
* verbose - returns _verbose
* is_connected - returns _is_connected

**Methods** :

* __init__

Sets MasterHead reference and stores _verbose, _secured parameters.

* connect

Connects to email server (specified via parameters host, port, user, passw). First fires event email_before_connect where parameters can be 
rewritten. Sets _client to imaplib client instance (using constructor IMAP4 or IMAP4_SSL depending on _secured) and connects to server 
(authentication using imaplib method login). Turns verbose mode if enabled (imaplib parameter set_debugl), not secured protocol is used by default.
After successful connection fires event email_after_connect and returns bool. Connection timeout is 10s by default (parameter timeout).

  .. code-block:: python
  
     from hydratk.lib.network.email.client import EmailClient
     
     c = EmailClient('IMAP')
     res = c.connect(host='imap.seznam.cz', port=143, user='hydra', passw='hydra')     

* disconnect

Disconnects from database using imaplib method shutdown and returns bool.

  .. code-block:: python
  
     res = c.disconnect()     
     
* email_count

Counts emails in mailbox on server using imaplib method select. Returns count.

  .. code-block:: python
  
     res = c.email_count()       
     
* list_emails

Lists email in mailbox on server using imaplib method search. Returns list of email ids.

  .. code-block:: python
  
     res = c.list_emails()     
     
* receive_email

Receives given email from server. First fires event email_before_receive_email where parameter msg_id can be rewritten.
Downloads email using imaplib method fetch and parses it. 

From: sender
To: recipient1,recipient2,...
CC: cc1,cc2,...
Subject: subject
Inbound message
message

After that method fires event email_after_receive_email and returns tuple (sender, recipients, cc, subject, message).

  .. code-block:: python
  
     # first email
     res = c.receive_email(1)
     
     # last email
     res = c.receive_email(c.email_count())         