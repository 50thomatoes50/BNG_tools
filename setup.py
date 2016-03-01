#!/usr/bin/env python
import subprocess

try:
    label = subprocess.check_output(["git", "describe", "--always"])
except WindowsError:
    raise Exception("Install git")

tags,hotfix,git_hash= label.strip("\n").split("-")

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