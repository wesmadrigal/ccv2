#!/usr/bin/env python
import bs4
import urllib2
import re
import json


def get_craigslist(location, title):
     
    if ',' in location:
        location = location.strip(location[location.find(','):])
    location = ''.join(re.findall(r'[a-zA-Z]+', location)).lower()
    # get the closest matching craigslist match
    mappings = json.loads( open('mappings.txt', 'r').read() ) 
    match_count = None
    for key in mappings.keys():
        count = 0
        for char in location:
            if char in key:
                count += 1
        if match_count:
            if count > match_count[1]:
                match_count = (key, count)
        else:
            match_count = (key, count)
    title, link = match_count[0], mappings[match_count[0]] 
    title = title.split(" ")
    if len(title) == 1:
        title = title[0].lower()
    else:
        title = "+".join(title).lower()
    res = urllib2.urlopen(link + '/search/jjj?catAbb=jjj&query={0}&zoomToPosting='.format(title))
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


def get_indeed_jobs(position, location):
    br = get_browser()
    base_url = 'http://www.indeed.com'
    br.open(base_url)
    br.select_form(nr=0)
    br.set_all_readonly(False)
    br.form['q'] = position
    br.form['l'] = location
    br.submit()
    # make some soup
    response = br.response().read()
    soup = BeautifulSoup(response)
    # find all the job elements
    jobs = drink_indeed_soup( soup )

    pagination = soup.find('div', {'class' : 'pagination'})

    pages = [ i for i in pagination.find_all('a', {'rel' : 'nofollow' }) ]
    pages = [ i for i in pages if i.string.isdigit() ]
    pages = [ base_url + i.get('href') for i in pages ]
    
    # for each page, extract jobs
    for page in pages:
        br.open( page )
        soup = BeautifulSoup(br.response().read())
        jobs.append( drink_indeed_soup( soup ) )
    
    return jobs
    
    
    
def drink_indeed_soup(soup):
    jobs = []
    link_base = 'http://www.indeed.com'
    job_elements = soup.find_all('div', {'class' : 'row'})
    for job in job_elements:
        try:
            job_obj = {}
            title_el = job.find('a', {'class', 'jobtitle'})
            title = title_el.get('title')
            link = link_base + title_el.get('href')
            company_el = job.find('span', {'class' : 'company'})
            company = company_el.string
            date_el = job.find('span', {'class' : 'date'})
            date = date_el.string
            location_el = job.find('span', {'class' : 'location'})
            location = location_el.string
            job_obj['title'] = title
            job_obj['link'] = link
            job_obj['company'] = company
            job_obj['location'] = location
            job_obj['date'] = date
            jobs.append( job_obj )
        except:
            continue
    return jobs

def get_monster(position, location):
    pass


def get_careerbuilder(position, location):
    pass



