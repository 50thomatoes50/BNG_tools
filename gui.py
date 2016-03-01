#!/usr/bin/env python

import Tkinter,ttk,tkMessageBox,tkFont

class choose(Tkinter.Tk):
    def __init__(self,files):
        Tkinter.Tk.__init__(self)
        self.title("Choose the map")
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
            "Thread quit earlier.\n The report may not exist."
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
    c = choose( ("test","test2"))
    c.mainloop()
    print "quit=", c.quit_val
    print "selected", c.var, c.Combobox.current()
    c.destroy()
    
    c = reportWorking("truc.mis",-1,test=True)
    c.mainloop()