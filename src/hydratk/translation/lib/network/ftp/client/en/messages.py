# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.ftp.client.en.messages
   :platform: Unix
   :synopsis: English language translation for FTP client messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {
    'htk_ftp_unknown_protocol' : ["Unknown protocol: '{0}'"],
    'htk_ftp_connecting'       : ["Connecting to server: '{0}'"],
    'htk_ftp_connected'        : ["Connected successfully"],
    'htk_ftp_unknown_method'   : ["Unknown method for protocol: '{0}'"],
    'htk_ftp_disconnected'     : ["Disconnected from server"],
    'htk_ftp_not_connected'    : ["Not connected to server"],
    'htk_ftp_list_dir'         : ["Listing directory: '{0}'"],
    'htk_ftp_change_dir'       : ["Changing to directory: '{0}'"],
    'htk_ftp_cur_dir'          : ["Working directory is: '{0}'"],
    'htk_ftp_downloading_file' : ["Downloading file: '{0}'"],
    'htk_ftp_unknown_dir'      : ["Unknown directory: '{0}'"],
    'htk_ftp_file_downloaded'  : ["File downloaded"],
    'htk_ftp_uploading_file'   : ["Uploading file : '{0}'"],
    'htk_ftp_unknown_file'     : ["Unknown file: '{0}'"],
    'htk_ftp_file_uploaded'    : ["File uploaded"],  
    'htk_ftp_deleting_file'    : ["Deleting file: '{0}'"],
    'htp_ftp_file_deleted'     : ["File deleted"],
    'htk_ftp_making_dir'       : ["Making directory: '{0}'"],
    'htk_ftp_dir_made'         : ["Directory made"],
    'htk_ftp_removing_dir'     : ["Removing directory: '{0}'"],
    'htk_ftp_dir_removed'      : ["Directory removed"]   
}
