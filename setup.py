#!/usr/bin/env python
import subprocess,re,os,sys
from cx_Freeze import setup, Executable
 

try:
    label = subprocess.check_output(["git", "describe", "--always", "--tags"])
except WindowsError:
    raise Exception("Install git")

splited = label.strip('\n').split('-')
print splited

if len(splited)==1:
    tags = splited[0]
    hotfix = "0"
elif len(splited)>1:
    tags = splited[0]
    hotfix = splited[1]
else:
    print splited
    raise Exception("Unknown")

__version__ = tags + "." + hotfix

__version_long__ = tags + " hotfix " + hotfix

#describe don't give the right thing (add a g)
git_hash =subprocess.check_output(["git", "rev-parse", "master"]).strip("\n")
git_hash_short = git_hash[:7]



with open("_version.py","w") as f:
    fw=f.write
    fw("""__version__ = "%s.%s"\n"""%(tags, hotfix))
    fw("""__version_long__ = "%s hotfix %s"\n"""%(tags ,hotfix))
    fw("""git_hash= "%s" \n"""%(git_hash))
    fw("""git_hash_short= "%s" \n"""%(git_hash_short))
    
    
    
    
    
base = None
if sys.platform == "win32":
    #base = "Win32GUI"
    base = "Console"

executables = [
    Executable("reporter.py",
               base=base,
               icon="image/icon.ico"
    ),
    Executable("BeamNG_Tools.py",
               base=base,
               icon="image/icon.ico"
    ),
    Executable("windows_integration.py",
               base=base,
    )
]

include_files=[]
include_files.append("LICENSE")
include_files.append("readme.md")

#this loop get all files in the directory array to be coped to tha build directory
for toCopy in ["image","theme"]:
	for root, dirs, files in os.walk( toCopy , topdown=True):
		for name in files:
			fpath = os.path.join(root, name)
			include_files.append( (fpath,fpath) )

buildOptions = dict(
    optimize = 2,
    includes=[],
    packages=[],
    include_files=include_files,
    excludes= [],
    zip_includes=[],
    include_msvcr = True,
    silent = True
    )

setup(
    name = "BeamNG tools",
    version = "0.1.0",
    description = " Tools to help BeamNG.Drive modders http://50thomatoes50.github.io/BNG_tools/",
    options=dict(build_exe=buildOptions),
    executables = executables
)