#main file

import os,sys
import gui,reporter

if __name__ == '__main__':
    l = gui.launcher()
    l.setCallback(reporter.RunReporter)
    l.mainloop()