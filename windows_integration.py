#!/usr/bin/env python

import os,sys,argparse,tkMessageBox,platform

def install():
    h =_winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\.btr")
    #_winreg.SetValue(h, r"", _winreg.REG_SZ, "BeamNG tools Report File")
    _winreg.SetValueEx(h, r"Content Type", None, _winreg.REG_SZ, "application/json")
    _winreg.SetValue(h, r"DefaultIcon", _winreg.REG_SZ, os.getcwd()+"\\image\\icon.ico")
    
    if getattr(sys, 'frozen', False):
        _winreg.SetValue(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT\shell\open\command", _winreg.REG_SZ, os.getcwd()+"\\BeamNG_Tools.exe --dispreport \"%1\"")
        _winreg.SetValue(h, r"", _winreg.REG_SZ, "BNGTOOL.DISPREPORT")
    else:
        _winreg.SetValue(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT.DEV\shell\open\command", _winreg.REG_SZ, sys.executable + " " + os.getcwd() + "\\BeamNG_Tools.py --dispreport \"%1\"")
        _winreg.SetValue(h, r"", _winreg.REG_SZ, "BNGTOOL.DISPREPORT.DEV")


def uninstall():
    try:
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT\shell\open\command")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT\shell\open")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT\shell")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT")
    except WindowsError:
        pass
    try:
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT.DEV\shell\open\command")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT.DEV\shell\open")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT.DEV\shell")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\BNGTOOL.DISPREPORT.DEV")
    except WindowsError:
        pass
    
    try:
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\.btr\DefaultIcon")
        _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\.btr")
    except WindowsError:
        pass


if __name__ == '__main__':
    if platform.system() != "Windows":
        print "You aren't running Python on Windows\n This script may not work"
        tkMessageBox.showerror (
            "Error",
            "You aren't running Python on Windows\n This script may not work"
        )
        sys.exit(-1)
        
    import _winreg,admin
    
    if not admin.isUserAdmin():
        admin.runAsAdmin()
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--install", help="", action="store_true")
    group.add_argument("-u", "--uninstall", help="", action="store_true")
    args = parser.parse_args()
    
    if args.install:
        install()
    elif args.uninstall:
        uninstall()
    else:
        try:
            h =_winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\CLASSES\.btr")
            
            if tkMessageBox.askyesno("Windows integration", "Do you want to UNinstall the file association?"):
                uninstall()
        except:
            if tkMessageBox.askyesno("Windows integration", "Do you want to install the file association?"):
                install()