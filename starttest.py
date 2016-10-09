import os
import re
import urllib
import urllib2
import logging
from subprocess import call
from prepare import getsetupinfo

lartlogger = logging.getLogger('Lart_i_desktop')

def downloadfile(local_dir, url):
    try:
        response = urllib2.urlopen(url)
        urllib.urlretrieve(url, local_dir)
    except:
        print '\tError download the file:', local_dir
        exit(1)


class PrepareIso(object):
    def __init__(self, setupxml, isolistfile):
        self.xml = setupxml
        self.isolist = isolistfile
     
    def parsingisolist(self):
        f = open(self.isolist, 'r')
        firstline = f.readline()
        isoname = re.findall(r"(.+)&&&&", firstline)   
        isoname = isoname[0] + ".iso"
        isolink = re.findall(r"&&&&(.+)", firstline)
        isolink = isolink[0] + '/' + isoname
        isoitem = [isoname, isolink]
        return isoitem

    def downloadiso(self):
        setupinfo = getsetupinfo(self.xml)
        isoitem = self.parsingisolist()
        print isoitem
        locatedir = os.path.join(setupinfo['xml_dict']['testtooldir'][0],
                                 isoitem[0])
        downloadfile(locatedir, isoitem[1])
      
a=PrepareIso('/home/desktop-iso/setup.xml', '/home/desktop-iso/testisolist')
a.downloadiso()   
