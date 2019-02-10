#!/usr/bin/env python

from __future__ import print_function
import sys

if sys.version_info >= (3,6):
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox as tkMessageBox
    from tkinter import font as tkFont
elif sys.version_info == (2,7):
    import Tkinter as tk
    import ttk
    import tkMessageBox
    import tkFont
else:
    raise RuntimeError("Python version not supported use [2.7, 3.6+], current = "+str(sys.version_info))

try:
    import _version
except ImportError:
    raise RuntimeError("You need to run this once 'python setup.py build'")

import webbrowser
from PIL import Image, ImageTk
from threading import Thread


def icon(obj):
    if sys.platform == 'win32':
        obj.iconbitmap(r'image\icon.ico',default=r'image\icon.ico')
    elif sys.platform == 'linux2':
        image = Image.open("image/icon_256.png")
        photo = ImageTk.PhotoImage(image)
        obj.iconphoto(True, photo)
    else:
        image = Image.open("image/icon_256.png")
        photo = ImageTk.PhotoImage(image)
        obj.iconphoto(True, photo)
        print("Unknown OS. Icon may not work")

class launcher(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("BeamNG Tools.py - Launcher")
        icon(self)
        self.resizable(0,0)

        #self.image = tk.PhotoImage(file="image\\icon_256.png")
        self.img = Image.open("image/icon_256.png")
        self.img.thumbnail((128,128), Image.ANTIALIAS)
        self.image= ImageTk.PhotoImage(self.img)
        self.btn_stat = ttk.Button(self, text="Check & Stats (only map)", image=self.image, compound="top")
        self.btn_stat.grid(row=0, column=0,padx=5, pady=5)

        self.btn_chkpack = ttk.Button(self, text="Pack", state=tk.DISABLED, image=self.image, compound="top")
        self.btn_chkpack.grid(row=0, column=1,padx=5, pady=5)

        self.btn_3 = ttk.Button(self, text="3", state=tk.DISABLED, image=self.image, compound="top")
        self.btn_3.grid(row=1, column=0,padx=5, pady=5)

        self.btn_4 = ttk.Button(self, text="4", state=tk.DISABLED, image=self.image, compound="top")
        self.btn_4.grid(row=1, column=1,padx=5, pady=5)

        self.verLbl = tk.Label(self, text = "BeamNG tools "+ _version.__version_long__)
        self.verLbl.grid(row=2, column=0,padx=5, pady=5, columnspan=2)
        self.verLbl.bind("<Button-1>", self.about)

    def setCallback(self,stat):
        self.btn_stat["command"] = stat

    def about(self,*args):
        a = about_win()

class about_win(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title("About - BeamNG Tools")
        self.grab_set()
        self.focus_set()
        self.resizable(0,0)

        self.img = Image.open("image/icon_256.png")
        self.image= ImageTk.PhotoImage(self.img)
        self.imlabel = tk.Label(self, image=self.image)
        self.imlabel.pack(padx=5, pady=5)

        self.lbl = tk.Label(self,text = "BeamNG Tools")
        self.lbl.pack(padx=5, pady=5)

        self.lblver = tk.Label(self,text = "Version " + _version.__version_long__ + " (" + _version.git_hash_short + ")")
        self.lblver.pack(padx=5, pady=5)

        self.lblc = tk.Label(self,text = "(C) 2017 Thomas PORTASSAU")
        self.lblc.pack(padx=5, pady=5)

        def site(event):
            webbrowser.open_new(r"https://github.com/50thomatoes50/BNG_tools")

        self.lblurl = tk.Label(self,text="github.com/50thomatoes50/BNG_tools", fg="blue", cursor="hand2")
        self.lblurl.pack(padx=5, pady=5)
        self.lblurl.bind("<Button-1>", site)

        self.bouton_quit = ttk.Button(self, text="Quit", command=self.destroy)
        self.bouton_quit.pack(side="right",padx=10,pady=10)

        def licwww():
            webbrowser.open_new(r"https://github.com/50thomatoes50/BNG_tools/blob/master/LICENSE")
        self.bouton_lic = ttk.Button(self, text="License",
                command=licwww)
        self.bouton_lic.pack(side="left",padx=10,pady=10)

        if getattr(sys, 'frozen', False):
            import BUILD_CONSTANTS
            self.lblbuild = tk.Label(self,text = "Build on '%s' the %s"%(BUILD_CONSTANTS.BUILD_HOST, BUILD_CONSTANTS.BUILD_TIMESTAMP))
            self.lblbuild.pack(padx=5, pady=5)

class loading_popup(tk.Toplevel):
    def __init__(self,title,mode,label):
        "mode = indeterminate || determinate"
        tk.Toplevel.__init__(self)
        self.title(title)
        self.grab_set()
        self.focus_set()
        self.resizable(0,0)
        icon(self)
        self.pbar = ttk.Progressbar(self, mode=mode, length=200)
        self.pbar.grid(row=0, column=0,padx=5, pady=5)

        self.lbl = tk.Label(self,text=label)
        self.lbl.grid(row=1, column=0,padx=5, pady=5)

        self.end = False

        self.protocol('WM_DELETE_WINDOW', self.close_checker)

        if mode == 'indeterminate':
            self.pbar.start()

    def close_checker(self):
        if self.end:
            self.quit()
        else:
            print("noclose")

    def start(self):
        self.pbar.start(50)

    def step(self,i):
        self.pbar.step(i)

    def set_progress(self,i):
        self.pbar['value']= i

    def stop(self):
        self.pbar.stop()

    def set_lbl(self,txt):
        self.lbl['text']=txt

    def dele(self ):
        self.end = True
        self.stop()
        self.quit()
        #self.destroy()



class choose(tk.Toplevel):
    def __init__(self,files):
        tk.Toplevel.__init__(self)
        self.title("Choose the map")
        self.grab_set()
        self.focus_set()
        self.resizable(0,0)
        icon(self)

        self.var = -1
        self.Combobox = ttk.Combobox(self, state="readonly")
        self.Combobox['values'] = files
        self.Combobox['width'] = 40
        self.Combobox.pack(padx=10,pady=10)

        self.hash = tk.IntVar()
        self.hashchkbox = ttk.Checkbutton(self, text="Generate file hash", variable=self.hash)
        self.hashchkbox.pack(padx=10,pady=10)

        self.quit_val = False

        self.bouton_quitter = ttk.Button(self, text="Quit", command=self.quitter)
        self.bouton_quitter.pack(side="left",padx=10,pady=10)

        self.bouton_cliquer = ttk.Button(self, text="Make Report",
                command=self.report)
        self.bouton_cliquer.pack(side="right",padx=10,pady=10)

        self.protocol('WM_DELETE_WINDOW', self.quitter)

    def quitter(self):
        self.quit_val = True
        self.quit()

    def report(self):
        if(self.Combobox.current()==-1):
            tkMessageBox.showerror (
            "Error",
            "You must select a map"
            )
        else:
            self.var = self.Combobox.current()
            self.quit()

class reportWorking(tk.Toplevel):
    def __init__(self,name,th,test=False):
        """th should be a working thread with
        .tasklist = []
        .step = 0 (not working, 1 first task)
        .progress"""
        tk.Toplevel.__init__(self)
        self.grab_set()
        self.focus_set()
        self.resizable(0,0)
        icon(self)

        self.t =th
        self.test=test
        self.title("Making report ...")


        self.font_normal=tkFont.Font(family='sans-serif',size=9)
        self.font_active=tkFont.Font(family='sans-serif',size=9,weight="bold")


        self.lf = ttk.Labelframe(self, text=name)
        self.lf.pack(padx=5,pady=5)

        if self.test:
            self.t.tasklist = [ "Parsing mission file",
                                "Exporting Tree Object and counting",
                                "Writing report"]

        ligne = 0
        self.tlist = []
        for t in self.t.tasklist:
            self.tlist.append( tk.Label(self.lf, text=t) )
            self.tlist[-1].pack(padx=4,pady=4, anchor=tk.W)

        self.taskprog = ttk.Progressbar(self, mode="determinate", length=200)
        self.taskprog.pack(padx=4,pady=4)

        self.totalprog = ttk.Progressbar(self, mode="determinate", length=200)
        self.totalprog.pack(padx=4,pady=4)

        self.t.start()
        if self.test:
            self.after(2000,self.refresh)
        else:
            self.after(200,self.refresh)

        self.protocol('WM_DELETE_WINDOW', self.close_checker)

    def close_checker(self):
        if not self.t.isAlive():
            self.quit()

    def refresh(self):

        if self.t.step<3 and not self.t.isAlive():
            tkMessageBox.showerror (
            "Error",
            "Thread quit earlier.\n The report may not exist.\n"+self.t.error
            )
            self.destroy()
            return

        try:
            if self.t.step > 0 : #working
                self.tlist[self.t.step-1].configure(font=self.font_active)

                if (self.t.step-2) >= 0 : #disable the previous one
                    for i in range(self.t.step-2):
                        self.tlist[i].configure(font=self.font_normal,state="disabled")

        except IndexError:
            self.t.join()
            self.destroy()

        try:
            self.taskprog['value'] = self.t.progress

            self.totalprog['value'] = self.t.progress / (len(self.t.tasklist)+1) + float(self.t.step)/(len(self.t.tasklist)+1)*100
        except tk.TclError:
            return
        #A TCL exception is raise when the thread is finished

        #print("%f %d/%d , %f,%f"%(self.t.progress, self.t.step, len(self.t.tasklist), self.taskprog['value'], self.totalprog['value']))

        if self.t.step == len(self.t.tasklist)+1:
            self.t.join()
            self.destroy()
            return
        else:
            self.after(200,self.refresh)



        """if self.t.step ==0:
            self.s1.configure(font=self.font_active)

        elif self.t.step == 1 :
            self.s1.configure(font=self.font_normal)
            self.s2.configure(font=self.font_active)
            self.s1.configure(state="disabled")
        elif self.t.step == 2 :
            self.s2.configure(state="disabled")
            self.s2.configure(font=self.font_normal)
            self.s3.configure(font=self.font_active)
        elif self.t.step == 3 :
            self.s3.configure(font=self.font_normal)
            self.s3.configure(state="disabled")
            self.t.join()
            self.destroy()
            return

        if self.t.step<3:
            self.after(200,self.refresh)"""

class DummyWorkThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.step=0
        self.tasklist = []
        for i in range(8):
            self.tasklist.append( "Test %d"%(i) )
        self.progress = 0

    def run(self):
        import time

        self.step = 1
        for a in range(len(self.tasklist)):
            self.progress = 0
            for b in range(9):
                self.progress +=10
                time.sleep(0.5)
            self.step += 1

if __name__ == '__main__':
    l = launcher()
    l.mainloop()

    ld = loading_popup("titre","indeterminate","Texte")
    ld.start()
    ld.after(2000, func=ld.dele)
    ld.mainloop()

    c = choose( ("test","test2"))
    c.mainloop()
    print("quit=", c.quit_val)
    print("selected", c.var, c.Combobox.current())
    c.destroy()

    t = DummyWorkThread()
    c = reportWorking("truc.mis",t)
    c.mainloop()