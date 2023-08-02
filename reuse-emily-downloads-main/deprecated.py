#checks for phrases in readmefiles only within last 5 commits

from datetime import date, time
import requests
from prometheus_client import start_http_server, Summary, Counter
from pydriller.repository import Repository  
from pydriller.metrics.process.commits_count import CommitsCount
import pydriller # Pydriller is the library we use to go through the commits on disc 
from git import Repo, Commit
import csv
import os
import pandas as pd
import numpy as np
from git import Repo
from builtins import any as b_any
import stscraper as scraper
import warnings
warnings.filterwarnings("ignore")

gh_api = scraper.GitHubAPI("INSERT TOKENS")
#testing the strudel scraper
gh_api.repo_info("mochini/cordova-plugin-aswebauthenticationsession")
os.chdir("/data3/emilyngu/")
#csv of unique slugs and basic info about them (date they peaked (if so), how many contributors, size of repo, etc.)
d = pd.read_csv("new.csv")
df = pd.DataFrame(d)
print(len(df))

jun18start = date(2018,12,31)
dec20end = date(2020,12,31)
startTime = time(7,00,00)
endTime = time(19,00,00)

monthStart_dates = {}
yearMonth_names = {}
for year in range (2018, 2021):
    for month in range(1, 13):
        monthidx = (year-2018)*12+month-1
        monthStart_dates[monthidx] = date(year, month, 1)
        yearMonth_names[monthidx] = f"{year}-{month}"


def getmonthidx(date):
            # checks to make sure commit is within 2015-jan - 2020-dec date range
            if date >= jun18start and date <= dec20end:
                # determines month index for date
                for monthidx in range(0, len(monthStart_dates)):
                    #checks to make sure it won't be out of range
                    if monthidx + 1 < len(monthStart_dates):
                        if date < monthStart_dates[monthidx + 1]:
                            return monthidx
                    # if this is true then its dec-20 and that is the monthindex that should be returned
                    elif monthidx + 1 >= len(monthStart_dates):
                        return monthidx
            return -1

df['test'] = -2
for i in range(0,len(df)):
    s = df['slug'][i]
    
    #################### clean up/filter the invalid slugs (slugs with more than one '/' in the repo name)
    try:
        if s.find('/tree/') != -1:
            s = s[0:s.find('/tree/')]
    except:
        pass
    try:
        if s.find('.git') != -1:
            s = s[0:s.find('.git')]
    except:
        pass
    try:
        if s.find('.com') != -1:
            s = s[s.find('.com')+5:]
    except:
        pass
    try:
        if s.find('.org') != -1:
            s = s[s.find('.org')+5:]
    except:
        pass
    try:
        if s[len(s)-1] == '/':
            s = s[0:len(s)-1]
    except:
        pass
    try:
        if '/master/' in s:
            s = s[0:s.find('/master/')]
    except:
        pass
    try:
        if '/packages/' in s:
            s = s[0:s.find('/packages/')]
    except:
        pass
    try:
        if '/main/' in s:
            s = s[0:s.find('/main/')]
    except:
        pass
    try:
        if s.find('/')!=-1:
            st = s.replace(s[s.find('/')], '_____')
    except:
        pass
    ####################
    
    
    ########## get the path of the repo
    a = "/data3/emilyngu/" + st
    df['dead'][i] = False
    count = 0
    flag = False

    ########## if path doesn't exist, clone it to tardigrade databse /data3/emilyngu
    if os.path.exists(a) == False:
        try:
            info = gh_api.repo_info(s)
            Repo.clone_from(info['html_url'], a)
            try:
                thing = len(list(Repository(a).traverse_commits()))
            except:
                df['test'][i] = -3
                df.to_csv("new.csv")
                continue 
        except:
            df['test'][i] = -3
            df.to_csv("new.csv")
            continue 

    try:
        
        #### if the repo has less than 20 commits, just look at the most recent 3 commits. otherwise, look at the most recent 10 commits
        totalCommits = len(list(Repository(a).traverse_commits()))
        if totalCommits == 0:
            continue
        elif totalCommits < 20:
            totalCommits = 3
        else:
            totalCommits = 10
    
        #traverse all commits for each project
        for commit in Repository(a).traverse_commits():
            if flag == True or count > totalCommits:
                break
             
            #only look at recent commits between 2018-12 to 2020-12 
            if getmonthidx(commit.author_date.date()) != -1:
                
                #look at commits to modified files
                for m in commit.modified_files:
                    
                    #look at modified files named "readme" or "README"
                    if m.filename.find("readme")!=-1 or m.filename.find("README")!=-1:
                        
                        ####### search for if phrases like deprecated, abandoned, no longer supported were added from the commit
                        out = [item for t in m.diff_parsed['added'] for item in t]
                        u = ''.join(str(v) for v in out)
                        if u.find("deprecated") != -1 or u.find("abandoned") != -1 or u.find("inactive") != -1 or u.find("terminated") != -1 or u.find("archived") != -1 or u.find("no longer maintained") != -1 or u.find("no longer supported") != -1 or u.find("no longer under development") != -1:
                            df['dead'][i] = True
                            print(df['slug'][i])
                            flag = True
                            break
                        break
                        #######
                count = count + 1 #increment our count, because we want to ultimately stop at the most recent 3-10 commits
 
        df['test'][i] = -1
    except:
        df['test'][i] = -3
    if df['test'][i] == -2:
        print(df['slug'][i] + str(i))
    df.to_csv("new.csv")
#    print(i)
