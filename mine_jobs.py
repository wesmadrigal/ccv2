#!/usr/bin/env python
import bs4
import urllib2
import re

class Job(object):
    def __init__(self, location, title, link, date, category):
        self.location = location
        self.title = title
        self.link = link
        self.date = date
        self.category = category

    def __repr__(self):
        return "\n".join([ self.location, self.title, self.link, self.date, self.category] )
    


def get_craigslist(location, title):
    if ',' in location:
        location = location.strip(location[location.find(','):])
    location = ''.join(re.findall(r'[a-zA-Z]+', location)).lower()
    title = title.split(" ")
    if len(title) == 1:
        title = title[0].lower()
    else:
        title = "+".join(title).lower()
    res = urllib2.urlopen('http://{0}.craigslist.org/search/jjj?catAbb=jjj&query={1}&zoomToPosting='.format(location, title))
    soup = bs4.BeautifulSoup(res.read()) 
    job_classes = []
 
    next_pages = soup.find_all(title="next page")
    while len(next_pages) != 0:

        divs = soup.find_all('div')
        content_div = [ j for j in divs if 'class' in j.attrs.keys() and j.attrs['class'][0] == 'content' ][0]
        jobs = content_div.find_all('p')
        for job in jobs:
            try:
                location = job.find_all('span')[4].findChild('small').string
            except:
                location = 'none'
            try:
                title = job.find_all('a')[1].string
                link = job.find_all('a')[1].get('href')
            except:
                title, link = ['none', 'none']
            try:
                date = job.find_all('span')[2].string
            except:
                date = 'none'
            try:
                category = job.find_all('a')[-1].string
            except:
                category = 'none'
     
            if location == 'none' and title == 'none' and link == 'none' and date == 'none' and category == 'none':
                continue
            else:
                job_classes.append( Job(location, title, link, date, category) )

        base_url = urllib2.urlparse.urlparse(res.geturl()).hostname
        try:
            next_page = 'http://' + base_url + next_pages[0].get('href') + '&sort=rel'
        except:
            break
        next_page = "+".join(next_page.split(" "))
        res = urllib2.urlopen(next_page)
        soup = bs4.BeautifulSoup(res.read())
        next_pages = soup.find_all(title='next page')
            
            
    return job_classes



def get_indeed(position, location):
    pass


def get_monster(position, location):
    pass


def get_careerbuilder(position, location):
    pass



