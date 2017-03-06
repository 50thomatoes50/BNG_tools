#!/usr/bin/env python
import re,os

class TorqueObject():
    def __init__(self,type,name,parent=None,source=""):
        self.type=type
        self.name=name
        self.parent=parent
        self.child=[]
        self.option={}
        self.source = source
        
    def repr(self):
        return "[TorqueObject instance "+self.type+" name="+self.name+"]"
    
    def add_option(self,name,value):
        if name == "internalName":
            self.name = value
        else:
            self.option[name]=value
        
def counter(obj):
    i=1
    for c in obj.child:
        if len(c.child)>0:
            i+=counter(c)
        else:
            i+=1
    return i
    
        
def count(obj):
    nb=0
    if type(obj) == type([]):
        for o in obj:
            nb+=counter(o)
        return nb
    elif type(obj) == type(TorqueObject(None,None)):
        return counter(obj)
        
def get_path(mis_path,p_path):
    if os.name is "nt":
        p_path.replace("/",os.sep)
    if not("levels" in p_path):
        return os.path.split(mis_path)[0] +"\\"+ p_path #relativ
    else:
        return mis_path[0:mis_path.find("levels")] + p_path
    
def is_BNGpath(fpath):
    """
    is it a path like Beamng whould use???????
    """
    if "unpacked" in fpath:
        try:
            fpath = get_BNGpath(fpath)
        except ValueError:
            return False
        
    fpath = os.path.normpath(fpath)
    a = fpath.split(os.sep)
    
    return a[0]=="art" or a[0]=="levels" or a[0] == "vehicles"
    
    
def get_BNGpath(fpath):
    """
    get the path like Beamng would use
    :warning: only use path from mods/unpacked
    """
    fpath = os.path.normpath(fpath)
    a = fpath.split(os.sep)
    try:
        return os.sep.join(a[a.index("unpacked")+2:])
    except ValueError:
        #if it's not in unpacked for repo
        if "levels" in fpath:
            return os.sep.join(a[a.index("levels"):])
        elif "vehicles" in fpath:
            return os.sep.join(a[a.index("levels"):])
        elif "art" in fpath:
            return os.sep.join(a[a.index("art"):])
        else:
            print "ValueError path not valid? (%s)"%(fpath)
            raise
    """
    if not("levels" in p_path) or "./" in p_path or ".\\" in p_path:
        return os.path.dirname(file_path[p_path.find("levels"):]) + os.sep + p_path #relative
    else:
        return p_path[p_path.find("levels"):] """
    
        
def join_BNGpath(file_path,p_path):
    """
    join the path to get a path like BeamNG would use
    file_path must point to the original file (TorqueObject.source)
    p_path can be any path (relative path / full path ...)
    """
    p_path = os.path.normpath(p_path)
    file_path = os.path.normpath(file_path)
    
    if is_BNGpath(p_path):
        return p_path
    else:
        return os.path.normpath( get_BNGpath(file_path) + os.sep + p_path )
    
    """if not("levels" in p_path) or "./" in p_path or ".\\" in p_path:
        return os.path.dirname(file_path[p_path.find("levels"):]) + os.sep + p_path #relative
    else:
        return p_path[p_path.find("levels"):] """
    
    
def get_filepath(tree):
    """get every files used by an TorqueObject"""
    
    """ Todo: retrieve the file using the object type instead of brute force checking """
    """if tree.option.has_key("fileName"):
        return tree.option["fileName"]
    elif tree.option.has_key("shapeName"):
        return tree.option["shapeName"]
    elif tree.option.has_key("texture"):
        return tree.option["texture"]
    elif tree.option.has_key("terrainFile"):
        return tree.option["terrainFile"]
    elif tree.option.has_key("dataFile"):
        return tree.option["dataFile"]"""
    try:
        if tree.type == "CloudLayer":
            return tree.option["texture"]
        elif tree.type == "WaterPlane":
            return (tree.option["rippleTex"],tree.option["foamTex"],tree.option["depthGradientTex"])
        elif tree.type == "TerrainBlock":
            return tree.option["terrainFile"]
        elif tree.type == "Forest":
            return tree.option["dataFile"]
        elif tree.type == "TSStatic":
            return tree.option["shapeName"]
    except KeyError:
        return False
        
    return None
 
def mission_parser(filename, option=False):
    root=[]
    trace=[]
    node=0
    level=-1
    if not os.path.isfile(filename):
        raise Exception("File is not valid : "+filename)
    with open( filename, "r") as f:
        for line in f:
            w = line.split()
            if len(w)==0 or w[0][0:2]=="//":
                continue
            elif w[0]=="new" or w[0]=="singleton":
                match = re.search(r"(\w+)(\ ?\(\ ?)(\w*)", w[1])
                if match:
                    node = TorqueObject(match.group(1),match.group(3),source=filename)
                    if level <0:
                        root.append(node)
                    else:
                        trace[level].child.append(node)
                    trace.append(node)
                    level+=1
                    
            elif w[0]=="};":
                level-=1
                if level >0:
                    trace.pop()
            else:
                if option:
                    match = re.search(r'(\S+)(\ ?\=\ ?\")(.+)(\"\;)', line)
                    if match and type(node) == type(TorqueObject(None,None)) :
                        node.add_option(match.group(1),match.group(3))
    return root

def disp(node,i,option=False):
    pre = "\t"*i
    print pre, node.repr()
    if option:
        for ok in node.option.keys():
            print pre,"\t%s = '%s';"%(ok,node.option[ok])
    for c in node.child:
        disp(c,i+1,option)


if __name__ == '__main__':
    print get_path("D:\\Users\\Thomas\\Documents\\BeamNG.drive\\mods\\unpacked\\wip.zip\\levels\\Carmageddon\\map.mis","art\\map.prefab")
    
    print get_path("D:\\Users\\Thomas\\Documents\\BeamNG.drive\\mods\\unpacked\\wip.zip\\levels\\Carmageddon\\map.mis","levels\\Carmageddon\\art\\map.prefab")

    
    """r= mission_parser("map.mis",True)
    disp(r[0],0,True)
    print count(r)
    
    r=mission_parser("D:\\Users\\Thomas\\Documents\\BeamNG.drive\\mods\\unpacked\\wip.zip\\levels\\Carmageddon\\map.mis")
    disp(r[0],0)
    print count(r)"""
    
    r=mission_parser("C:\\Users\\Administrator\\Documents\\BeamNG.drive\\mods\\unpacked\\IslandOfSpeed.zip\\levels\\Road of Speed\\art\\road\\materials.cs",True)
    disp(r[0],0)
    
    print "\n\n"
    
    print is_BNGpath("levels/Road of Speed/art/road/road-01_n.dds")