# -*- coding: utf-8 -*-

# Web Scraper for Indeed job postings
# Source: Michael Salmon's Medium post
# URL: https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b

import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

# Third attempt: Basic workaround
# Issue: Success!

max_results_per_city = 50

city_set = ["New+York+NY", "Seattle+WA", "San+Francisco+CA", "Washington+DC", "Atlanta+GA",
            "Boston+MA", "Austin+TX", "Cincinnati+OH", "Pittsburgh+PA"]

columns = ["summary"]

df = pd.DataFrame(columns = columns)

links = []

# Grab all job links from search results 
for city in city_set:
    for start in range(0, max_results_per_city, 10):
        page = requests.get("http://www.indeed.com/jobs?q=data+scientist&1=" + str(city) + "&start=" + str(start))
        time.sleep(1)
        soup = BeautifulSoup(page.text, "html.parser")
        for div in soup.find_all(name = "div", attrs = {"class":"row"}):
            for a in div.find_all(name = "a", attrs = {"data-tn-element":"jobTitle"}):
                links.append(a["href"])
                
base_url = "https://www.indeed.com/"

for link in links:
    # Get next empty row in data frame
    num = len(df) + 1
    
    summary = []
    page2 = requests.get(base_url + link)
    soup2 = BeautifulSoup(page2.text, "html.parser")
    # time.sleep(1)
    d = soup2.findAll("span", attrs = {"class":"summary"})
    for span in d:
        summary.append(span.text.strip())
    df.loc[num] = summary
    
df.to_csv("indeed_jobs2.csv", encoding = "utf-8")

    
"""
# Workaround
# Seems to collect full summary?

URL = "https://www.indeed.com/jobs?q=data%20scientist&l=New%20York%2C%20NY"
page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")

info = []
links = []
for div in soup.find_all(name = "div", attrs = {"class":"row"}):
    for a in div.find_all(name = "a", attrs = {"data-tn-element":"jobTitle"}):
        links.append(a["href"])
        
base_url = "https://www.indeed.com/"

for link in links:
    page2 = requests.get(base_url + link)
    soup2 = BeautifulSoup(page2.text, "html.parser")
    time.sleep(2)
    d = soup2.findAll("span", attrs = {"class":"summary"})
    for span in d:
        info.append(span.text.strip())
            
print(info[1])
"""

"""

# First attempt: Original Code
# Issue: Summary is truncated

max_results_per_city = 100

city_set = ["New+York+NY", "Seattle+WA", "San+Francisco+CA", "Washington+DC", "Atlanta+GA",
            "Boston+MA", "Austin+TX", "Cincinnati+OH", "Pittsburgh+PA"]

columns = ["city", "job_title", "company_name", "location", "summary", "salary"]

sample_df = pd.DataFrame(columns = columns)

for city in city_set:
    for start in range(0, max_results_per_city, 10):
        page = requests.get("http://www.indeed.com/jobs?q=data+scientist&l=" + str(city) + "&start=" + str(start))
        time.sleep(1)
        soup = BeautifulSoup(page.text, "lxml", from_encoding = "utf-8")
        for div in soup.find_all(name = "div", attrs = {"class":"row"}):
            num = (len(sample_df) + 1)          # Row num for df
            job_post = []                       # New job posting
            job_post.append(city)               # Append city from city_set       
            for a in div.find_all(name = "a", attrs = {"data-tn-element":"jobTitle"}):
                job_post.append(a["title"])     # Append job title
            company = div.find_all(name = "span", attrs = {"class":"company"})
            if len(company) > 0:                # Get company name
                for b in company:
                    job_post.append(b.text.strip())
            else:
                sec_try = div.find_all(name = "span", attrs = {"class":"result-link-source"})
                for span in sec_try:
                    job_post.append(span.text)
            c = div.findAll("span", attrs = {"class":"location"})
            for span in c:
                job_post.append(span.text)      # Append location of job
            d = div.findAll("span", attrs = {"class":"summary"})
            for span in d:                      # Append job summary
                job_post.append(span.text.strip())
            try:                                # Get job salary, if any
                job_post.append(div.find("nobr").text)
            except:
                try:
                    div_two = div.find(name = "div", attrs = {"class":"sjcl"})
                    div_three = div_two.find("div")
                    job_post.append(div_three.text.strip())
                except:
                    job_post.append("")
            sample_df.loc[num] = job_post

sample_df.to_csv("indeed_jobs.csv", encoding = "utf-8")
"""

"""
# Second attempt: Uses workaround
# Issue: Seems to stall
#        Also, it cannot accurately parse company and job title

max_results_per_city = 50

city_set = ["New+York+NY", "Seattle+WA", "San+Francisco+CA", "Washington+DC", "Atlanta+GA",
            "Boston+MA", "Austin+TX", "Cincinnati+OH", "Pittsburgh+PA"]

columns = ["company_name", "job_title", "summary"]

base_url = "https://www.indeed.com/"

df = pd.DataFrame(columns = columns)
links = []

for city in city_set:
    for start in range(0, max_results_per_city, 10):
        page = requests.get("http://www.indeed.com/jobs?q=data+scientist&1=" + str(city) + "&start=" + str(start))
        time.sleep(1)
        soup = BeautifulSoup(page.text, "html.parser")
        for div in soup.find_all(name = "div", attrs = {"class":"row"}):
            for a in div.find_all(name = "a", attrs = {"data-tn-element":"jobTitle"}):
                links.append(a["href"])
    
print(len(links))
            
for link in links:
    page2 = requests.get(base_url + link)
    soup2 = BeautifulSoup(page2.text, "html.parser")
    time.sleep(1)
    
    # Row num for df
    num = (len(df) + 1)
    job_post = []

    for c in soup2.findAll("span", attrs = {"class":"company"}):
        job_post.append(c)
    
    for b in soup2.findAll("b", attrs = {"class":"jobtitle"}):
        job_post.append(b)
        
    s = soup2.findAll("span", attrs = {"class":"summary"})
    for span in s:
        job_post.append(span.text.strip())
    
    if len(job_post) == 3:
        df.loc[num] = job_post
        print(num)
    
df.to_csv("indeed_jobs2.csv", encoding = "utf-8")

"""