#!/usr/bin/env python

from __future__ import print_function
from bs4 import BeautifulSoup as bs
import os, sys
if sys.version_info >= (3,6):
    import urllib.parse as urlparse
    import urllib.request as urllib2
elif sys.version_info == (2,7):
    import urlparse
    import urllib2
else:
    raise RuntimeError("Python version not supported use [2.7, 3.6+], current = "+str(sys.version_info))

import urllib,zipfile,shutil
import reporter

class RepoMod():
    """analyse a mod from the BeamNg Repo

    id can be an str or int"""

    def __init__(self, id,hash=False):
        self.modinfo       = dict()
        self.modurl        = ""
        self.url           = ""
        self.hash          = hash

        if type(id) == type(0):
            self.id = id
        else:
            try:
                self.id = int(id)
            except TypeError:
                print("Wrong type of argument!")
                raise

    def run(self):
        self.url = "https://www.beamng.com/resources/.%d/"%(self.id)
        soup = bs( urllib2.urlopen( self.url ) , "html.parser")

        if not os.path.exists(".temp"):
            os.mkdir(".temp")


        #http://stackoverflow.com/questions/185936/delete-folder-contents-in-python

        for the_file in os.listdir(".temp"):
            file_path = os.path.join(".temp", the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


        try:
            self.modfileurl = "https://www.beamng.com/" + soup.find_all(class_="downloadButton ")[0].a['href']

            self.modinfo['repo_author']       = soup.find_all(class_="author")[0].a.string
            self.modinfo['repo_author_id']    = soup.find_all(class_="author")[0].a["href"].split(".")[-1].strip("/ -")

            def getVersion(t):
                return t.parent.name == u"h1" and "muted" in t['class']

            self.modinfo['repo_version']      = soup.find_all(getVersion)[0].string
        except:
            print("failed to get mod info")
            raise

        print("repo info = ", self.modinfo)

        print("Downloading the mod ...")
        urllib.urlretrieve ( self.modfileurl , ".temp/tmp.zip" )

        print("Extracting the mod ...")
        zip_ref = zipfile.ZipFile(".temp/tmp.zip", 'r')
        zip_ref.extractall(".temp/")
        zip_ref.close()

        scanth = reporter.ScanMisThread(".temp")
        scanth.start()
        scanth.join()

        if scanth.done and scanth.mis_files:
            for mis in scanth.mis_files:
                print("Analysing ", mis)
                th = reporter.MakeReportThread( mis,
                                                extinfo=self.modinfo,
                                                origin_path = os.path.abspath(".temp"),
                                                fileHash = self.hash)
                th.start()
                th.join()
        else:
            print("MIS scan failed!")


if __name__ == '__main__':
    m = RepoMod(207)
    m.run()