import urllib2
import re
import os
import logging
from subprocess import Popen, PIPE
from prepare import getsetupinfo

lartlogger = logging.getLogger('Lart_i_desktop')

def downloadfile(local_dir, url):
    try:
        response = urllib2.urlopen(url)
        urllib.urlretrieve(url, local_dir)
    except:
        print '\tError download the file:', local_dir
        exit(1)

class CheckUpdate(object):

    def get_htmlcontent(self, xmlurl, remode):
        try:
            html_Context = urllib2.urlopen(xmlurl).read()
        except urllib2.HTTPError:
            lartlogger.error('%s is open failed' % xmlurl) # need report this error
        html_Context = unicode(html_Context, 'utf-8')
        return re.findall(r"%s" % remode, html_Context)

    def getisolist(self, setupxml):
        setupinfo = getsetupinfo(setupxml)
        xmlurl = setupinfo['xml_dict']['isourl'][0]
       #  remode = "href=\"(.+).iso\">" # iso url
        remode = "href=\"(.+?)/\">[r/b/R/B]" # http://koji.isoft.zhcn.cc/iso/isoft4.0/
        isopathlist = self.get_htmlcontent(xmlurl, remode)
        isolist = []
        linklist = []
        for k, isotype in enumerate(isopathlist):
            remode = "href=\"(.+).iso\">"
            link = xmlurl + isotype
            isoname = self.get_htmlcontent(link, remode)
            isolist.append(isoname)
            linklist.append(link)
        print linklist
        testiso = isolist[-1][0]
        testlink = linklist[-1]
        testitem = testiso + "&&&&" + testlink
        isolistfile = os.path.join(setupinfo['xml_dict']['testtooldir'][0],
                                   "testisolist")
        f = open(isolistfile, 'a+')
        Type="Y"
        for line in f.xreadlines():
            if line.strip('\n') == testiso:
                Type="N"
                break
        if Type == "Y":
            f.write('%s\n' % testitem)

test = CheckUpdate()
test.getisolist('/home/desktop-iso/setup.xml')
