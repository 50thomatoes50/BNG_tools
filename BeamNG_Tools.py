#main file

from __future__ import print_function
import os,sys
import argparse
import webbrowser
if sys.version_info >= (3,6):
    from tkinter import messagebox as tkMessageBox
elif sys.version_info == (2,7):
    import tkMessageBox
else:
    raise RuntimeError("Python version not supported use [2.7, 3.6+], current = "+str(sys.version_info))
import gui,reporter,repo

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--makereport", help="The file which will be processed", type=str)
    group.add_argument("--dispreport", help="Display a report", type=str)
    group.add_argument("--repo", help="Make a report for a repo mod", type=int)
    parser.add_argument("--no-gui", help="GUI will not be started", action="store_true")
    parser.add_argument("--hash", help="Generate file hash (only for make report)", action="store_true")
    args = parser.parse_args()

    if args.dispreport:
        if( os.getcwd().startswith(os.path.dirname(args.dispreport))  ):
            with open("redirect.html","w") as f:
                f.write("<html><script>window.location.href = 'theme/default/json.html?file=../../%s';</script></html>"%(os.path.basename(args.dispreport)))
                webbrowser.open("redirect.html")
        else:
            tkMessageBox.showerror (
                "Error",
                "Don't support opening file outside the executable path"
                )
    elif args.makereport:
        #print("report = "+args.report)
        #print("gui = " + str(args.no_gui))
        if not os.path.exists(args):
            if args.no_gui:
                print("The file don't exist")
                sys.exit(-2)
            else:
                tkMessageBox.showerror (
                "Error",
                "The file don't exist"
                )
        else:
            #work
            pass
    elif args.repo:
        rp = repo.RepoMod(args.repo, hash=args.hash)
        rp.run()
    else:
        l = gui.launcher()
        l.setCallback(reporter.RunReporter)
        l.mainloop()