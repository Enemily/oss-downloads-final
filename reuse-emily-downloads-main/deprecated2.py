#checks for phrases like "deprecated" and "no longer maintained" in first few lines of readme

from git import Repo
from builtins import any as b_any
#import stscraper as scraper
import pandas as pd
import os

os.chdir("/data3/emilyngu")
#csv of unique slugs and basic info about them (date they peaked (if so), how many contributors, size of repo, etc.)
data = pd.read_csv("newDeprecated2.csv")
df = pd.DataFrame(data)
print(len(df))

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
    except: pass
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
    if s.find('/')!=-1:
        st = s.replace(s[s.find('/')], '_____')
    ####################
    
    ########## get the path of the repo
    a = ""
    dir2 = '/data2/christian/npm/repos/' + st
    dir3 = '/data2/christian/npm/repos2/' + st
    df['dead'][i] = False
    if os.path.exists(dir2) or os.path.exists(dir3) == True or os.path.exists(a) == True:
        if os.path.exists(dir2):
            stri = dir2
        elif os.path.exists(dir3) == True:
            stri = dir3
        else:
            stri = a
    ##########

    ##### access files of the repo
        for root, dirs, files in os.walk(stri):
            for file in files:
                #### only look for files named "readme" or "README"
                if file.find("readme")!=-1 or file.find("README")!=-1:
                    dir = stri + '/'+ file
                    try:
                        with open(dir, 'r') as fp:
                            ##### only look at the first portion of the readme text (first 10% of the readme)
                            li = fp.readlines()
                            limit = int((0.1) * len(li))
                            li = li[0:limit]
                            #####
                            
                            # if found the phrases, set our "dead" variable in to true indicating the project had some indication of being dead through the phrases
                            df['dead'][i] = any("roject is deprecated" in string for string in li) or any("repo is deprecated" in string for string in li) or any("repository is deprecated" in string for string in li) or any("repo has been deprecated" in string for string in li) or any("repository has been deprecated" in string for string in li) or any("project has been deprecated" in string for string in li) or any("project is no longer maintained" in string for string in li) or any("repo is no longer maintained" in string for string in li) or any("repository is no longer maintained" in string for string in li)  or any("project is no longer supported" in string for string in li) or any("repo is no longer supported" in string for string in li) or any("repository is no longer supported" in string for string in li) or any("bandoned" in string for string in li) or any("rchived" in string for string in li) or any("no longer active" in string for string in li)
                            if df['dead'][i]:
                                print(df['slug'][i] + "," + str(i))
                                break
                    except:
                        pass
                    break
      #####
    
    ####d# on't try to understand this: just some minor error checking/saving to csv
    if i%500==0:
        print(i)
    df['hi'][i] = -5
    if len(df) < 30000:
        print("STOP: " + df['slug'][i] + ", "+i)
    df.to_csv("newDeprecated2.csv")
