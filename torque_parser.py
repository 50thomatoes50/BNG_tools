#!/usr/bin/env python
import re

class TorqueObject():
    def __init__(self,type,name,parent=None):
        self.type=type
        self.name=name
        self.parent=parent
        self.child=[]
        
    def repr(self):
        return "[TorqueObject instance "+self.type+" name="+self.name+"]"
        
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
        
        

def mission_parser(filename):
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
    return root

def disp(node,i):
    pre = "\t"*i
    print pre, node.repr()
    for c in node.child:
        disp(c,i+1)


if __name__ == '__main__':
    r= mission_parser("map.mis")
    disp(r[0],0)
    print count(r)
    
    r=mission_parser("D:\\Users\\Thomas\\Documents\\BeamNG.drive\\mods\\unpacked\\wip.zip\\levels\\Carmageddon\\map.mis")
    disp(r[0],0)
    print count(r)