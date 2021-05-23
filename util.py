#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import datetime
import sys

import requests
import settings
#python3 -m pip install requests
class Util:
      
    def logstr(string):
        osdirname, filename = os.path.split(os.path.abspath(__file__))
        logdirname = osdirname+"/logs/"
        today = datetime.datetime.now() 
        logfile_name = "log" + today.strftime("%Y%m%d") +".text"

        if not os.path.exists(logdirname):
            os.makedirs(logdirname)

        #dirname = settings.options["LogPath"]
        log_file = logdirname+""+logfile_name
        f = open(log_file, "a")
        os.chmod(log_file, 0o777)
        
        #print(settings.options["Mouse"])

        if isinstance(string, list):
            str1 = ','.join(str(e) for e in string)
            string = str1

        log_string=os.environ.get('USER')+" ["+today.strftime('%Y-%m-%d %H:%M:%S')+"] "+str(string)
        f.write(log_string + "\n")
        f.close()
        return False
    
    def log_exeption(inst):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        osdirname, filename = os.path.split(os.path.abspath(__file__))
        logdirname = osdirname+"/logs/"
        today = datetime.datetime.now() 
        logfile_name = "log" + today.strftime("%Y%m%d") +".text"

        if not os.path.exists(logdirname):
            os.makedirs(logdirname)

        #dirname = settings.options["LogPath"]
        
        log_file = logdirname+""+logfile_name
        f = open(log_file, "a")
        os.chmod(log_file, 0o777)
        
        string = str(exc_type)+", "+str(fname)+", "+str(exc_tb.tb_lineno)+" , "+str(inst)

        log_string=os.environ.get('USER')+" ["+today.strftime('%Y-%m-%d %H:%M:%S')+"] "+str(string)
        f.write(log_string + "\n")
        f.close()
        return False
        