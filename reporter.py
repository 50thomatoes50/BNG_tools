#!/usr/bin/env python
import sys,os,platform,datetime ,json,webbrowser, tkMessageBox
from threading import Thread
import gui,torque_parser,_version 
     

class CaseInsensitiveDict(dict):
    """Basic case insensitive dict with strings only keys."""

    proxy = {}

    def __init__(self, data={}):
        self.proxy = dict((k.lower(), k) for k in data)
        for k in data:
            self[k] = data[k]

    def __contains__(self, k):
        return k.lower() in self.proxy

    def __delitem__(self, k):
        key = self.proxy[k.lower()]
        super(CaseInsensitiveDict, self).__delitem__(key)
        del self.proxy[k.lower()]

    def __getitem__(self, k):
        key = self.proxy[k.lower()]
        return super(CaseInsensitiveDict, self).__getitem__(key)

    def get(self, k, default=None):
        return self[k] if k in self else default

    def __setitem__(self, k, v):
        super(CaseInsensitiveDict, self).__setitem__(k, v)
        self.proxy[k.lower()] = k

    
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

class ScanMisThread(Thread):

    def __init__(self, fpath , cbre, cbend):
        Thread.__init__(self)
        self.fpath      = fpath
        self.debug      = False
        self.mis_files  = []
        self.cbre       = cbre
        self.cbend      = cbend
        self.done       = False
        
    def run(self):
        if self.debug:
            print "\n ### scan_mis() ###"
        
        for root, dirs, files in os.walk(self.fpath):
            level = root.replace(self.fpath, '').count(os.sep)
            for f in files:
                ext = os.path.splitext(f)[1]
                if ext == ".mis":
                    self.mis_files.append(root.replace(self.fpath, '')+"\\"+f)
                    self.cbre( "Found %d map(s)"%(len(self.mis_files)) )
                    if self.debug:
                        print f
                    
        self.done = True
        self.cbend()

the_tree = []
indice = 0
realcounter = 0
obj_list_used = CaseInsensitiveDict()
msg_list=[]

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
            bngpath = os.path.normpath( os.path.dirname(mis_path) + os.sep + fileName )
            if not obj_list_used.has_key(bngpath):
                obj_list_used[bngpath] = {"name": c.name, "type":c.type, "nb_used": nb}
            else:
                obj_list_used[bngpath]["nb_used"] += nb
            

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
        if torque_parser.is_BNGpath( tree.option["fileName"] ):
            path = tree.option["fileName"]
        else:
            path = torque_parser.join_BNGpath(mis_path, tree.option["fileName"])
        child_doublon(tree.child, path,id_p)
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
    #return json.dumps(the_tree) #Production
    return the_tree

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
    """ a Thread class that make a ruport on the map `fname`
    extinfo is a dict
    origin_path is by default in User Documents folder"""

    def __init__(self, fname,
                 extinfo={},
                 origin_path = os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\"
                 ):
        Thread.__init__(self)
        self.fname=fname
        self.extinfo = extinfo
        self.step=0
        self.error=""
        self.origin_path = origin_path
        
    def run(self):
        #try:
        now = datetime.datetime.now()      
        #reportName = "report_"+os.path.split(self.fname)[1]+"_"+now.strftime("%Y-%m-%d_%H.%M.%S")+".html"
        reportName = os.path.split(self.fname)[1]+"_"+now.strftime("%Y-%m-%d_%H.%M.%S")+".btr"
        
        
        r = torque_parser.mission_parser(self.origin_path + self.fname,True)
        """except:
            print "parse error"
            return"""
        self.step=1
        objnb = torque_parser.count(r)
        
        tree_str = make_tree(r[0],self.origin_path + self.fname)
        
        
        data = {}
        data['info'] = {"version":
                            {"report":1,
                                "soft":{
                                   "number":_version.__version_long__,
                                   "git_hash":_version.git_hash,
                                   "git_hash_short":_version.git_hash_short
                                }
                            },
                        "date":now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%H:%M:%S"),
                        "author":"",
                        "name":self.fname,
                        "extinfo":self.extinfo
                        }        
        
        map_dir = os.path.dirname(self.origin_path + self.fname)
        
        mat=[]
        
        for root, dirs, files in os.walk( map_dir , topdown=True):
            for name in files:
                fpath = os.path.join(root, name)
                #bngpath = fpath[fpath.find("levels"):]
                bngpath = torque_parser.get_BNGpath(fpath)
                if not( bngpath in obj_list_used.keys() ):
                    #add this files
                    if name == "materials.cs":
                        obj_list_used[bngpath] = {"type": "Torque Script (Material)","nb_used": 1}
                        mat += torque_parser.mission_parser(fpath,True)
                    elif name.endswith(".cs"):
                        obj_list_used[bngpath] = {"type": "Torque Script","nb_used": 1}
                    elif name.endswith(".json"):
                        if name == "info.json" and root == map_dir:
                            obj_list_used[bngpath] = {"type": "JSON (map info)","nb_used": 1}
                            with open(fpath) as data_file:    
                                data['info']['info'] = json.load(data_file)
                                for ip in data['info']['info']['previews']:
                                    if not obj_list_used.has_key(bngpath):
                                        obj_list_used[bngpath] = {"type":"Picture (map preview)", "nb_used": 1}
                                    else:
                                        obj_list_used[bngpath]["nb_used"] += 1
                        elif name == "map.json" and root == map_dir:
                            obj_list_used[bngpath] = {"type": "JSON (map path)","nb_used": 1}
                    elif name.endswith(".mis.decals"):
                        obj_list_used[bngpath] = {"type":"Mission decals", "nb_used": 1}
                    elif name.endswith(".cdae"):
                        obj_list_used[bngpath] = {"type":"Mesh cache", "nb_used": 0}
                        msg_list.append( ("warning","Mesh cache shouldn't be packed in the mod (%s)"%(bngpath) ) )
                    else:
                        obj_list_used[bngpath] = {"type": "...","nb_used": 0}
        
            
        for m in mat:
            tex_opt = []
            if m.type == "CubemapData":
                tex_opt = ["cubeFace[0]", "cubeFace[1]" "cubeFace[2]", "cubeFace[3]", "cubeFace[4]", "cubeFace[5]"]
            elif m.type == "Material":
                tex_opt = ["specularMap[0]","diffuseMap[0]","normalMap[0]","specularMap[1]","diffuseMap[1]","normalMap[1]"]
            elif m.type == "TerrainMaterial":
                tex_opt = []
            else:
                msg_list.append( ("error","Material script object type unknown : %s in %s"%(m.type,m.source) ) )
                
            for top in tex_opt:
                if top in m.option.keys():
                    bpath = torque_parser.join_BNGpath( os.path.dirname(m.source), m.option[top] )
                    if os.path.splitext(bpath)[1] == "":
                        #no ext -> find the file by guessing the ext
                        mExtFound = False
                        for ext in [".dds", ".png", ".jpg", ".jpeg", ".bmp"]:
                            if bpath+ext in obj_list_used.keys():
                                bpath+=ext
                                obj_list_used[bpath]["type"] = "Texture"
                                obj_list_used[bpath]["nb_used"] += 1
                                mExtFound = True
                                break
                            
                        if not(mExtFound):
                            msg_list.append( ("error",
                                              "Material <a href='#mat:%s'>%s</a> texture not found = %s (from %s)"%
                                              (m.name, m.name, bpath, m.source)
                                            ) )
                    
                    #extention is present in path so check it
                    else:
                        if bpath in obj_list_used.keys():
                            obj_list_used[bpath]["type"] = "Texture"
                            obj_list_used[bpath]["nb_used"] += 1
                        else:
                            msg_list.append( ("error",
                                              "Material <a href='#mat:%s'>%s</a> texture not found = %s (from %s)"%
                                              (m.name, m.name, bpath, m.source)
                                            ) )
                        
        #Unused Object!!!!!!!!!!!!!!!!!!!!
        unused_obj = 0                
        for o in obj_list_used.keys():
            if obj_list_used[o]["nb_used"] == 0:
                unused_obj +=1
                
        if unused_obj:
            msg_list.append( ("warning","There is %d unused object"%(unused_obj) ) )
        
        self.step = 2
        
        #tranform every TorqueObject in dict so python can serialiate them in json
        mat_json=[]
        for m in mat:
            mat_json.append(m.__dict__)
        
        data['report']= {"tree":tree_str,
                 "objCount":realcounter,
                 "res":obj_list_used,
                 "msg":msg_list,
                 "mat":mat_json}
        
        with open(reportName, 'w') as outfile:
            json.dump(data, outfile, indent=4)
        
        """with open("theme\\default\\index.html", "r") as s:
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
                    
                    """
    
        self.step = 3
        #webbrowser.open(reportName)
        #webbrowser.open( "%s\\theme\\default\\json.html?file=../../%s&fake=file.html"%(os.getcwd(),reportName) )
        with open("redirect.html","w") as f:
            f.write("<html><script>window.location.href = 'theme/default/json.html?file=../../%s';</script></html>"%(reportName))
            webbrowser.open("redirect.html")
            
def RunReporter():
    a = gui.loading_popup("Scanning ...", "indeterminate", "Scanning...")
    #fichier = scan_mis(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\")
    th = ScanMisThread(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked\\", a.set_lbl, a.dele)
    th.start()
    #th.join()
    a.mainloop()
    a.destroy()
    if th.done:
        fichier = th.mis_files
    else:
        tkMessageBox.showerror (
            "Error",
            "The scan may have gone wrong.\nSome files can be missing in the list."
        )
    
    c = gui.choose(fichier)
    c.mainloop()
    if(c.quit_val):
        c.destroy()
    else:
        c.destroy()
        print "Mission files selcted :", fichier[c.var], "(",c.var,")"
        #make_report(fichier[c.var])
        #os.system("pause")
        th = MakeReportThread(fichier[c.var])
        th.isAlive
        c = gui.reportWorking(fichier[c.var],th)
        c.mainloop()

if __name__ == '__main__':
    if platform.system() != "Windows":
        print "You aren't running Python on Windows\n This script may not work"
        tkMessageBox.showerror (
            "Error",
            "You aren't running Python on Windows\n This script may not work"
        )
        sys.exit(-1)
    #print os.environ
    if not(os.path.exists(os.environ['USERPROFILE']+"\\Documents\\BeamNG.drive\\mods\\unpacked")):
        tkMessageBox.showerror (
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

    
    
    
    