#!/usr/bin/env python
import sys,os,platform,datetime ,json,webbrowser
from threading import Thread
import gui,torque_parser,_version
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
obj_list_used ={}
msg_list=()

def child_doublon(childs,mis_path,parent):
    global the_tree,indice,realcounter
    done = []
    for c in childs:
        if c.type != 'TSStatic':
            child_tree(c,mis_path,parent)
        elif c.option["shapeName"] not in done:
            nb=0
            for ca in childs:
                if not ca.option.has_key("shapeName"):
                    continue
                if c.option["shapeName"] == ca.option["shapeName"]:
                    nb+=1
                    realcounter+=1
            
            name = "%s(%s)"%(c.type,os.path.split(c.option["shapeName"])[1])
            id_p = name
            the_tree.append( {"id":id_p,"name":name,"parent":parent,"value":nb} )
            done.append(c.option["shapeName"])
            
            fileName = torque_parser.get_filepath(c)
            if not obj_list_used.has_key(fileName):
                obj_list_used[fileName] = {"name": c.name, "type":c.type, "nb_used": nb}
            else:
                obj_list_used[fileName]["nb_used"] += nb
            

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
    
    fileName = torque_parser.get_filepath(tree)
    if fileName:
        if type(fileName) is type(''):
            if not obj_list_used.has_key(fileName):
                obj_list_used[fileName] = {"name": tree.name, "type":tree.type, "nb_used": 1}
            else:
                obj_list_used[fileName]["nb_used"] += 1
        elif type(fileName) is tuple:
            for f in fileName:
                if not obj_list_used.has_key(f):
                    obj_list_used[f] = {"name": tree.name, "type":tree.type, "nb_used": 1}
                else:
                    obj_list_used[f]["nb_used"] += 1
        else:
            print "filename type =="+str(type(fileName))
    if fileName == False:
        msg_list.append( ("warning","Object %s(%s) have a missing property"%(tree.name,tree.type)) )
        
        
    if tree.type == "Prefab":
            child_doublon(tree.child,mis_path,id_p)
    else:
        if len(tree.child):
            child_doublon(tree.child,mis_path,id_p)
        #for c in tree.child:
            
    


def make_tree(tree,mis_path):
    #the_tree = []
    #indice = 0
    #realcounter = 0
    obj_list_used =[]
    child_tree(tree,mis_path)
    #return json.dumps(the_tree, indent=4) # debugging data
    return json.dumps(the_tree) #Production

def make_report(fname):
    global report_step
    try:
        r = torque_parser.mission_parser(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + fname,True)
    except:
        print "parse error"
        return
    report_step=1
    objnb = torque_parser.count(r)
    
    tree_str = make_tree(r[0],os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + fname)
    
    obj_list_used_html = ""
    for k in obj_list_used.keys():
        obj_list_used_html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%i</td></tr>\n"%(k,"_",obj_list_used[k].type,obj_list_used[k]["nb_used"])
    
    msg_list_html=""
    for i in msg_list:
        msg_list_html += "<tr class='.%s'><td>%s</td><tr>\n"%(i[0],i[1])
    
    
    now = datetime.datetime.now()
    reportName = "report_"+os.path.split(fname)[1]+"_"+now.strftime("%Y-%m-%d_%H.%M.%S")+".html"
    
    report_step = 2
    with open("theme\\default\\index.html", "r") as s:
        with open(reportName, "w") as d:
            for l in s:
                tmp = l
                if "%map_name%" in l:
                    tmp = tmp.replace("%map_name%",fname)
                if "%object_count%" in l:
                    tmp = tmp.replace("%object_count%",str(realcounter))
                if "%mat_count%" in l:
                    tmp = tmp.replace("%mat_count%",str(0))
                if "%tree_data%" in l:
                    tmp = tmp.replace("%tree_data%",tree_str)
                if "%git_hash%" in l:
                    tmp = tmp.replace("%git_hash%",_version.git_hash_short)
                if "%hash_long%" in l:
                    tmp = tmp.replace("%hash_long%",_version.git_hash)
                if "%version_number%" in l:
                    tmp = tmp.replace("%version_number%",_version.__version_long__)
                
                d.write(tmp)
    report_step = 3
    webbrowser.open(reportName)
    os.system("pause")
    

class MakeReportThread(Thread):

    def __init__(self, fname):
        Thread.__init__(self)
        self.fname=fname
        self.step=0
        
    def run(self):
        #try:
        r = torque_parser.mission_parser(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + self.fname,True)
        """except:
            print "parse error"
            return"""
        self.step=1
        objnb = torque_parser.count(r)
        
        tree_str = make_tree(r[0],os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\" + self.fname)
        
        obj_list_used_html = ""
        for k in obj_list_used.keys():
            try:
                os.path.split(k)
                obj_list_used_html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%i</td></tr>\n"%(os.path.split(k)[0],os.path.split(k)[1],obj_list_used[k]["type"],obj_list_used[k]["nb_used"])
            except :
                print sys.exc_info()
        
        msg_list_html=""
        for i in msg_list:
            msg_list_html += "<tr class='.%s'><td>%s</td><tr>\n"%(i[0],i[1])
        
        now = datetime.datetime.now()      
        reportName = "report_"+os.path.split(self.fname)[1]+"_"+now.strftime("%Y-%m-%d_%H.%M.%S")+".html"
        
        self.step = 2
        with open("theme\\default\\index.html", "r") as s:
            with open(reportName, "w") as d:
                for l in s:
                    tmp = l
                    if "%map_name%" in l:
                        tmp = tmp.replace("%map_name%",self.fname)
                    if "%object_count%" in l:
                        tmp = tmp.replace("%object_count%",str(realcounter))
                    if "%mat_count%" in l:
                        tmp = tmp.replace("%mat_count%",str(0))
                    if "%tree_data%" in l:
                        tmp = tmp.replace("%tree_data%",tree_str)
                    if "%git_hash%" in l:
                        tmp = tmp.replace("%git_hash%",_version.git_hash_short)
                    if "%hash_long%" in l:
                        tmp = tmp.replace("%hash_long%",_version.git_hash)
                    if "%version_number%" in l:
                        tmp = tmp.replace("%version_number%",_version.__version_long__)
                    if "%obj_table%" in l:
                        tmp = tmp.replace("%obj_table%",obj_list_used_html)
                    if "%msg_table%" in l:
                        tmp = tmp.replace("%msg_table%",msg_list_html)
                        
                    
                    d.write(tmp)
        self.step = 3
        webbrowser.open(reportName)
    

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
    #make_report(fichier[c.var])
    #os.system("pause")
    th = MakeReportThread(fichier[c.var])
    th.isAlive
    c = gui.reportWorking(fichier[c.var],th)
    c.mainloop()

    
    
    
    