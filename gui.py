#!/usr/bin/env python

import Tkinter,ttk,tkMessageBox,tkFont
from sys import platform
from PIL import Image, ImageTk

def icon(obj):
    if platform == 'win32':
        obj.iconbitmap(r'image\icon.ico',default=r'image\icon.ico')    
    elif platform == 'linux2':
        image = Image.open("image/icon_256.png")
        photo = ImageTk.PhotoImage(image)
        obj.iconphoto(True, photo)
    else:
        image = Image.open("image/icon_256.png")
        photo = ImageTk.PhotoImage(image)
        obj.iconphoto(True, photo)
        print "Unknown OS. Icon may not work"
        
class launcher(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.title("BeamNG Tools.py - Launcher")
        icon(self)
        
        #self.image = Tkinter.PhotoImage(file="image\\icon_256.png")
        self.img = Image.open("image/icon_256.png")
        self.img.thumbnail((128,128), Image.ANTIALIAS)
        self.image= ImageTk.PhotoImage(self.img)
        self.btn_stat = ttk.Button(self, text="Stats (only map)", image=self.image, compound="top")
        self.btn_stat.grid(row=0, column=0,padx=5, pady=5)
        
        self.btn_chkpack = ttk.Button(self, text="Check mod and pack", state=Tkinter.DISABLED, image=self.image, compound="top")
        self.btn_chkpack.grid(row=0, column=1,padx=5, pady=5)
        
        self.btn_3 = ttk.Button(self, text="3", state=Tkinter.DISABLED, image=self.image, compound="top")
        self.btn_3.grid(row=1, column=0,padx=5, pady=5)
        
        self.btn_4 = ttk.Button(self, text="4", state=Tkinter.DISABLED, image=self.image, compound="top")
        self.btn_4.grid(row=1, column=1,padx=5, pady=5)


class loading_popup(Tkinter.Tk):
    def __init__(self,title,mode,label):
        "mode = indeterminate || determinate"
        Tkinter.Tk.__init__(self)
        self.title(title)
        icon(self)
        self.pbar = ttk.Progressbar(self, mode=mode, length=200)
        self.pbar.grid(row=0, column=0,padx=5, pady=5)
        
        self.lbl = Tkinter.Label(self,text=label)
        self.lbl.grid(row=1, column=0,padx=5, pady=5)
        
    def start(self):
        self.pbar.start(50)
        
    def step(self,i):
        self.pbar.step(i)
        
    def stop(self):
        self.pbar.stop()
        
    def set_lbl(self,txt):
        self.lbl['test']=txt
    

class choose(Tkinter.Tk):
    def __init__(self,files):
        Tkinter.Tk.__init__(self)
        self.title("Choose the map")
        icon(self)
        self.var = -1
        self.Combobox = ttk.Combobox(self, state="readonly")
        self.Combobox['values'] = files
        self.Combobox['width'] = 40
        self.Combobox.pack(padx=10,pady=10)
        
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
            
class reportWorking(Tkinter.Tk):
    def __init__(self,name,th,test=False):
        Tkinter.Tk.__init__(self)
        icon(self)
        self.t =th
        self.test=test
        self.title("Making report ...")
        
        
        self.font_normal=tkFont.Font(family='sans-serif',size=9)
        self.font_active=tkFont.Font(family='sans-serif',size=9,weight="bold")
        
        
        lf = ttk.Labelframe(self, text=name)
        lf.pack(padx=5,pady=5)
        
        self.s1 = Tkinter.Label(lf, text="Parsing mission file")
        self.s1.pack(padx=4,pady=4, anchor=Tkinter.W)
        self.s2 = Tkinter.Label(lf, text="Exporting Tree Object and counting")
        self.s2.pack(padx=4,pady=4, anchor=Tkinter.W)
        self.s3 = Tkinter.Label(lf, text="Writing report")
        self.s3.pack(padx=4,pady=4, anchor=Tkinter.W)
        
        self.t.start()
        if self.test:
            self.after(2000,self.refresh)
        else:
            self.after(200,self.refresh)
            
    def refresh(self):
        if self.test:
            self.t+=1
            
        if self.t.step<3 and not self.t.isAlive():
            tkMessageBox.showerror (
            "Error",
            "Thread quit earlier.\n The report may not exist.\n"+t.error
            )
            self.destroy()
            return
            
        if self.t.step ==0:
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
            self.after(200,self.refresh)
        
if __name__ == '__main__':
    l = launcher()
    l.mainloop()
    
    ld = loading_popup("titre","indeterminate","Texte")
    ld.start()
    ld.mainloop()
    
    c = choose( ("test","test2"))
    c.mainloop()
    print "quit=", c.quit_val
    print "selected", c.var, c.Combobox.current()
    c.destroy()
    
    c = reportWorking("truc.mis",-1,test=True)
    c.mainloop()