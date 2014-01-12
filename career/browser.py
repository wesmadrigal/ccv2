#!/usr/bin/env python
import mechanize
import cookielib

def get_browser():
    br = mechanize.Browser()
    cookiejar = cookielib.LWPCookieJar()
    br.set_cookiejar(cookiejar)
    br.set_handle_robots(False)
    br.set_debug_http(True)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_debug_redirects(True)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br
