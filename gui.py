#!/usr/bin/env python

import Tkinter,ttk,tkMessageBox

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
        
if __name__ == '__main__':
    c = choose( ("test","test2"))
    c.mainloop()
    print "quit=", c.quit_val
    print "selected", c.var, c.Combobox.current()
    c.destroy()