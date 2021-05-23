#import from libs
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
import time 
import sys
import traceback

#import from project
import settings
from util import *
from capture import *

class FaultTolerantTk(tk.Tk):
    def report_callback_exception(self, exc, val, tb):
        self.destroy_unmapped_children(self)
        messagebox.showerror('Error!', val)

    # NOTE: It's an optional method. Add one if you have multiple windows to open
    def destroy_unmapped_children(self, parent):
        """
        Destroys unmapped windows (empty gray ones which got an error during initialization)
        recursively from bottom (root window) to top (last opened window).
        """
        children = parent.children.copy()
        for index, child in children.items():
            if not child.winfo_ismapped():
                parent.children.pop(index).destroy()
            else:
                self.destroy_unmapped_children(child)
                
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        tk.Tk.report_callback_exception = self.show_error

        self.master.protocol("WM_DELETE_WINDOW", self.say_quite)

        self.pack()
        self.logged_secs = 0
        self.start_timer = False
        
        #Create application window
        self.create_widgets()
        
        self.c = Capture()

        
    '''
    def report_callback_exception(self, exc, val, tb):
        Util.logstr("report_callback_exception")
        self.destroy_unmapped_children(self)
        messagebox.showerror('Error!', val)

    #NOTE: It's an optional method. Add one if you have multiple windows to open
    def destroy_unmapped_children(self, parent):
        """
        Destroys unmapped windows (empty gray ones which got an error during initialization)
        recursively from bottom (root window) to top (last opened window).
        """
        children = parent.children.copy()
        for index, child in children.items():
            if not child.winfo_ismapped():
                parent.children.pop(index).destroy()
            else:
                self.destroy_unmapped_children(child)    
    '''
    
    def show_error(self, *args):
        err = traceback.format_exception(*args)
        Util.logstr("Exception"+str(err))
        messagebox.showerror('Exception',err)
    

    def create_widgets(self):
        try:
            self.btn_start = tk.Button(self.master)
            self.btn_start.place(x=5,y=10)
            self.btn_start["text"] = "Start"
            self.btn_start["fg"] = "green"
            self.btn_start["command"] = self.say_toggle
            
            self.lbl_ttime = tk.Label(text="", fg="green", font=("Helvetica", 10))
            self.lbl_ttime.place(x=70,y=20)
            self.lbl_ttime.configure(text=str(self.logged_secs))

            self.btn_quit = tk.Button(self.master, text="QUIT", fg="red",
                                command=self.say_quite)
            #self.btn_quit.pack(side="bottom")
            self.btn_quit.place(x=140,y=10)

            self.btn_dbug = tk.Button(self.master)
            self.btn_dbug["text"] = "debug"
            self.btn_dbug["command"] = self.debug
            #self.btn_dbug.pack(side="top")
            self.btn_dbug.place(x=210,y=10)
            
            
        except Exception as e:
            Util.log_exeption(e)
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno , e)

    def debug(self):
        try:
            Util.logstr("debug")
            #self.c.seethreads()
            #self.update_time()
            osdirname, filename = os.path.split(os.path.abspath(__file__))
            messagebox.askquestion(filename, osdirname)
            #Util.logstr("debug t:"+str(t))


        except Exception as e:
            Util.log_exeption(e)           
   
    def convert(self,seconds):
        try:
            return time.strftime("%H:%M:%S", time.gmtime(seconds))
        except Exception as e:
            Util.log_exeption(e)

    def say_toggle(self):
        try:
            if(not self.c.timer_start):
                self.say_start()
                self.c.logaction("Logging", "Start")
            else:
                self.say_stop()
                self.c.logaction("Logging", "Stop")

        except Exception as e:
            Util.log_exeption(e)

    def say_start(self):
        try:
            Util.logstr("Timeer Capturing: Start")
            self.c.timer_start = True
            self.c.threading_start = True
            self.btn_start["text"] = "Stop"
            self.btn_start["fg"] = "red"
            #self.update_clock()
            self.update_time()
            

        except Exception as e:
            Util.log_exeption(e)

    def say_stop(self):
        try:
            Util.logstr("Timer Capturing: Stop")
            self.c.timer_start = False
            self.btn_start["text"] = "Start"
            self.btn_start["fg"] = "green"
            self.c.threading_start = False
            self.c.terminate()
            #self.c.check_ideal()
            
        except Exception as e:
            Util.log_exeption(e)        

    def say_quite(self):
        try:
            res = messagebox.askquestion("askquestion", "Are you sure?")
            Util.logstr("Timeer Capturing: Quite:"+res)
            if(res == "yes"):
                self.say_stop()
                self.c.daemon_start =False
                self.master.destroy()
        except Exception as e:
            Util.log_exeption(e)
 
    '''
    def watch_ideal(self):
        try:
            Util.logstr("watch_ideal")
        except Exception as e:
            Util.log_exeption(e)    
    '''

    def update_time(self):
        try:
            if(self.c.timer_start):
                #Util.logstr("update_time")
                #self.c.seconds_cal = int(self.c.seconds_cal) + 1
                total_secs = self.c.calc_time()
                display_time = self.convert(total_secs);
                #Util.logstr(str(display_time))
                self.lbl_ttime.configure(text=str(display_time))
                self.after(1000, self.update_time)
                if(self.c.isideal == True):
                    self.say_stop()
                    self.c.logaction("AutoIdeal", "Stop")
                    Util.logstr("isideal:"+str(self.c.isideal))
                    res = messagebox.askquestion("askquestion", "Are you working?")

                    Util.logstr("Are you working?"+res)

                    if(res == "yes"):
                        self.c.isideal = False
                        self.say_start()
                        self.c.logaction("AutoIdeal", "Start")
                    else:
                        self.c.isideal = True

        except Exception as e:
            Util.log_exeption(e)
    '''
    def update_clock(self):
        try:
            if(self.start_timer):
                self.logged_secs = int(self.logged_secs) + 1
                display_time = self.convert(self.logged_secs);
                self.lbl_ttime.configure(text=str(display_time))
                self.after(1000, self.update_clock)
                if(self.c.isideal == True):
                    self.say_stop()
                    self.c.logaction("AutoIdeal", "Stop")

        except Exception as e:
            Util.log_exeption(e)
    '''

     
  
root = tk.Tk()
root.title("Capture21")
root.geometry("400x100")
#root = FaultTolerantTk()
app = Application(master=root)
app.mainloop()
