
import time 
import os 

#capture screenshot
import pyautogui

#for threading
import threading

#popup message box
from tkinter import messagebox

#try catch
import traceback

#import from project
import settings
from util import *

#from pynput.mouse import Button, Listener
from pynput import mouse
#from pynput.keyboard import Key, Listener
from pynput import keyboard

class Capture:
    def __init__(self):
        Util.logstr("Capture init...")
        self.threading_start = True #self.strartthreading_start = True # Start all treads on init 
        self.daemon_start = True #self.masterstart = True
        self.isideal = False
        self.timer_start = False
        self.seconds_cal = 0
        self.last_action_time = 0
        
        if(settings.options["ScreenShot"]):
            self.thread_ss = threading.Thread(target=self.start_ss, args=(), name='start_ss')
            if not self.thread_ss.is_alive():
                self.thread_ss.start()
    
        if(settings.options["KeyBorad"]):
            self.thread_kb = threading.Thread(target=self.start_kb, args=(), name='thread_kb')
            if not self.thread_kb.is_alive():
                self.thread_kb.start()

        if(settings.options["Mouse"]):
            self.thread_mu = threading.Thread(target=self.start_mu, args=() ,name='thread_mu')
            if not self.thread_mu.is_alive():
                self.thread_mu.start()

        self.thread_ideal = threading.Thread(target=self.check_ideal, args=() ,name='thread_ideal')
        self.thread_ideal.start()
        
        time.sleep(1)
        
        # Stop Loggong activity once all thread started
        self.threading_start = False
      
    def terminate(self):
        Util.logstr("Capture:stop activity from threads")
        self.threading_start = False

        #time.sleep(1)
        #self.thread_ss.join()

        #if(settings["KeyBorad"]):
        #self.thread_kb.join()

        #if(settings["Mouse"]):
        #self.thread_mu.join()
    
    def start_ss(self):
        Util.logstr("Screenshot Capturing: init start")
        while self.daemon_start:
            sleeptime = int(settings.options["ImageTimeInSec"])
            time.sleep(sleeptime)
            if self.threading_start:
                if(settings.options["ScreenShot"]):
                    #Util.logstr("Screenshot Capturing: init start")
                    now = time.strftime("%d-%m-%Y" + 'T' + "%H-%M-%S")
                    #im1 = pyautogui.screenshot()

                    osdirname, filename = os.path.split(os.path.abspath(__file__))
                    ssdirname = osdirname+"/screenshot/"

                    if not os.path.exists(ssdirname):
                        os.makedirs(ssdirname)

                    #img_name = settings.options["DataPath"]+"screenshot/"+now+'my_screenshot.png'
                    img_name = ssdirname+now+'my_screenshot.png'
                    Util.logstr("Screenshot Captured :"+img_name)
                    im2 = pyautogui.screenshot(img_name)
                    #Util.logstr("Screenshot Capturing:"+str(threading.currentThread()))
                    

                

    def check_ideal(self):
        #Util.logstr("Ideal Watch: "+str(self.threading_start))
        Util.logstr("Ideal Watch: init start")
        while self.daemon_start:
            while self.threading_start:
                time.sleep(10)
                if(self.last_action_time):
                    now = datetime.datetime.now()
                    diff = now - self.last_action_time
                    Util.logstr("Ideal Time:"+str(int(diff.total_seconds()))+" Criteria:"+str(settings.options["IdealTimeOutSec"]))
                    if(int(diff.total_seconds()) > int(settings.options["IdealTimeOutSec"])):
                        self.isideal = True

    def start_kb(self):
        Util.logstr("Keyboard Capturing: init start")
        if(self.threading_start):
            listener = keyboard.Listener(on_press=self.getKey)
            listener.start()
            #Util.logstr("current_kb:"+str(threading.currentThread()))
        
    def getKey(self,key):
        if(self.threading_start):
            key = self.fixKey(key)
            self.logaction("Keybord","keypressed")

    def fixKey(self,key):
        #logaction("Key","Clicked")
        key = str(key)
        if key == 'Key.space':
            return ' '
        elif key == 'Key.enter':
            return '\n'
        return key

    def start_mu(self):
        Util.logstr("Mouse Capturing: init start")
        if(self.threading_start):
            #with mouse.Listener(on_click=self._mouseclick) as listener:
            #    listener.join()
            listener = mouse.Listener(on_click=self._mouseclick)
            listener.start()
            #Util.logstr("current-mu:"+str(threading.currentThread()))
    

    def _mouseclick(self,x, y, button, pressed):
        if pressed and self.threading_start:
            self.logaction("Mouse","Clicked")
    
    def calc_time(self):
        #Util.logstr("calc_time")
        self.seconds_cal = int(self.seconds_cal) + 1
        return self.seconds_cal

    def logaction(self,string,action):
        #senddata(string,action)
        dirname, filename = os.path.split(os.path.abspath(__file__))
        actdirname = dirname+"/logs/"

        today = datetime.datetime.now()
        self.last_action_time  =  today
        logfile_name = "action" + today.strftime("%Y%m%d") +".text"
        log_file = actdirname+logfile_name
        f = open(log_file, "a")
        os.chmod(log_file, 0o777)
        
        log_string=today.strftime('%Y-%m-%d %H:%M:%S')+","+str(string)+","+str(action)
        f.write(log_string + "\n")
        f.close()
        return False

    def seethreads(self):
        Util.logstr("seethreads>thread_ideal:"+str(self.thread_ideal.is_alive()))
        Util.logstr("seethreads>thread_ss :"+str(self.thread_ss.is_alive()))
        Util.logstr(str(threading.active_count()))
        Util.logstr(str(threading.enumerate()))
        Util.logstr(str(threading.currentThread()))
