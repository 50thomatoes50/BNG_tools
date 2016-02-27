#!/usr/bin/env python
import re

class TorqueObject():
    def __init__(self,type,name,parent=None):
        self.type=type
        self.name=name
        self.parent=parent
        self.child=[]
        self.option={}
        
    def repr(self):
        return "[TorqueObject instance "+self.type+" name="+self.name+"]"
    
    def add_option(self,name,value):
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
        
        

def mission_parser(filename, option=False):
    root=[]
    trace=[]
    node=0
    level=-1
    with open( filename, "r") as f:
        for line in f:
            w = line.split()
            if len(w)==0 or w[0][0:2]=="//":
                continue
            elif w[0]=="new":
                match = re.search("(\w*)(\()(\w*)", w[1])
                if match:
                    node = TorqueObject(match.group(1),match.group(3))
                    if level <0:
                        root.append(node)
                    else:
                        trace[level].child.append(node)
                    trace.append(node)
                    level+=1
                    
            elif w[0]=="};":
                level-=1
                trace.pop()
            else:
                if option:
                    match = re.search("""(\w+)(\ =\ ")(.+)(";)""", line)
                    if match:
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
    r= mission_parser("map.mis",True)
    disp(r[0],0,True)
    print count(r)
    
    r=mission_parser("D:\\Users\\Thomas\\Documents\\BeamNG.drive\\mods\\unpacked\\wip.zip\\levels\\Carmageddon\\map.mis")
    disp(r[0],0)
    print count(r)