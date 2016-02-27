#!/usr/bin/env python
import sys,os,platform,datetime ,json,webbrowser
import gui,torque_parser
try:
    import Tkinter
except:
    print "Tkinter is missing"
    sys.exit(-1)
    
debug = True
    
def scan_mis(fpath):
    if debug:
        print "\n ### scan_mis() ###"
    mis_files =[]
    for root, dirs, files in os.walk(fpath):
        level = root.replace(fpath, '').count(os.sep)
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext == ".mis":
                mis_files.append(root.replace(fpath, '')+"\\"+f)
                if debug:
                    print f
                
    return mis_files

the_tree = []
indice = 0
realcounter = 0

def child_tree(tree,mis_path,parent=None):
    global the_tree, indice,realcounter
    realcounter+=1
    id_p=""
    name=""
    if tree.type == "TSStatic":
        name = "%s(%s)"%(tree.type,os.path.split(tree.option["shapeName"])[1])
        id_p = name + "_%i"%(indice)
        indice +=1
    elif tree.type == "Prefab":
        id_p = "%s(%s)"%(tree.type,tree.option["fileName"])
        name = id_p
        tree.child = torque_parser.mission_parser(torque_parser.get_path(mis_path,tree.option["fileName"]),True)
    elif tree.name == "":
        id_p = "%s(No_name_%i)"%(tree.type,indice)
        name = id_p
        indice +=1
    else:
        id_p = "%s(%s)"%(tree.type,tree.name)
        name = id_p
        
    if parent == None:
        the_tree.append( {"id":id_p,"name":name} )
    else:
        the_tree.append( {"id":id_p,"name":name,"parent":parent,"value":len(tree.child)+1} )
        
    for c in tree.child:
        child_tree(c,mis_path,id_p)
        


def make_tree(tree,mis_path):
    child_tree(tree,mis_path)
    return json.dumps(the_tree, indent=4)

def make_report(fname):
    try:
        r = torque_parser.mission_parser(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + fname,True)
    except:
        print "parse error"
        return
    objnb = torque_parser.count(r)
    
    tree_str = make_tree(r[0],os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + fname)
    now = datetime.datetime.now()
    reportName = "report_"+os.path.split(fname)[1]+"_"+now.strftime("%Y-%m-%d_%H.%M.%S")+".html"
    with open("theme\\default\\index.html", "r") as s:
        with open(reportName, "w") as d:
            for l in s:
                if "%map_name%" in l:
                    d.write(l.replace("%map_name%",fname))
                elif "%object_count%" in l:
                    d.write(l.replace("%object_count%",str(realcounter)))
                elif "%mat_count%" in l:
                    d.write(l.replace("%mat_count%",str(0)))
                elif "%tree_data%" in l:
                    d.write(l.replace("%tree_data%",tree_str))
                else:
                    d.write(l)
                    
    webbrowser.open(reportName)
    os.system("pause")
    
    torque_parser.disp(r[0],0,False)
    

if __name__ == '__main__':
    if platform.system() != "Windows":
        print "You aren't running Python on Windows\n This script may not work"
        tk.tkMessageBox.showerror (
            "Error",
            "You aren't running Python on Windows\n This script may not work"
        )
        sys.exit(-1)
    #print os.environ
    if not(os.path.exists(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked")):
        tk.tkMessageBox.showerror (
            "Error",
            "BeamNG.drive\\mods\\unpacked !!!!!!!!!!"
        )
        sys.exit(-1)
        
    fichier = scan_mis(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\")
    
    c = gui.choose(fichier)
    c.mainloop()
    if(c.quit_val):
        c.destroy()
        sys.exit(0)
    c.destroy()
    print "Mission files selcted :", fichier[c.var], "(",c.var,")"
    make_report(fichier[c.var])
    os.system("pause")

    
    
    
    