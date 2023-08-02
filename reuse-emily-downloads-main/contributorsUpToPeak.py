#finds total number contributors up to last commit before peak

# import csv
# import requests
# import os
# import pandas as pd
# import numpy as np
# import stscraper as scraper
# from git import Repo
# from datetime import datetime
# import warnings
# warnings.filterwarnings("ignore")

# os.chdir("/data3/emilyngu")
# d = pd.read_csv("newArchived.csv")
# df = pd.DataFrame(d)

# #gh_api = scraper.GitHubAPI(" INSERT TOKENS")
# gh_api = scraper.GitHubAPI("INSERT TOKENS")

# #issueEvents = gh_api.repo_issue_events("mochini/cordova-plugin-aswebauthenticationsession")
# #issueEvents = gh_api.repo_contributors("mochini/cordova-plugin-aswebauthenticationsession")
# s = "feathersjs/feathers-query-filters"
# #d = pd.DataFrame(gh_api.repo_contributors(s)).set_index('user')

# issueEvents = gh_api.repo_contributors(s)

# for i in range(0,len(df)):
#     s = df['slug'][i]
#     try:
#         if s.find('/tree/') != -1:
#             s = s[0:s.find('/tree/')]
#     except:
#         pass
#     try:
#         if s.find('.git') != -1:
#             s = s[0:s.find('.git')]
#     except:
#         pass
#     try:
#         if s.find('.com') != -1:
#             s = s[s.find('.com')+5:]
#     except:
#         pass
#     try:
#         if s.find('.org') != -1:
#             s = s[s.find('.org')+5:]
#     except:
#         pass
#     try:
#         if s[len(s)-1] == '/':
#             s = s[0:len(s)-1]
#     except:
#         pass
#     try:
#         if '/master/' in s:
#             s = s[0:s.find('/master/')]
#     except:
#         pass
#     try:
#         if '/packages/' in s:
#             s = s[0:s.find('/packages/')]
#     except:
#         pass
#     try:
#         if '/main/' in s:
#             s = s[0:s.find('/main/')]
#     except:
#         pass

#     st = df['lastCommit'][i]
#     if i == 0:
#         age = df['age'][i]
#         datePeak = int(st[0:4] + st[5:7])
#     if isinstance(st, type(str)):
#         datePeak = int(st[0:4] + st[5:7])
#         age = df['age'][i]
#     sum =0 
#     try:
#         d = pd.DataFrame(gh_api.repo_contributors(s)).set_index('user')
#         d.columns = pd.to_datetime(d.columns, unit='s')
#         for column in d:
#             col = column.strftime('%Y-%m')
#             val = int(col[0:4] + col[5:7])
#             if val <= datePeak:
#                 sum+= d[column].sum()
#             else:
#                 break
#         df['contributorsToLastComm'][i] = sum
#         if i%2==0:
#             print("hi")
#         print(df['slug'][i] + " " + str(i))
#     except:
#         #print(df['slug'][i] + " " + str(i))
#         df['contributorsToLastComm'][i] = -1 
#     df['hi'][i] = -1
#     df.to_csv("newArchived.csv")
#     if i%2==0:
#         print(i)

import csv
import requests
import os
import pandas as pd
import numpy as np
import stscraper as scraper
from git import Repo
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

os.chdir("/data3/emilyngu")
#csv of unique slugs and basic info about them (date they peaked (if so), how many commits, size of repo, etc.)
d = pd.read_csv("pydrillerCommits.csv")
df = pd.DataFrame(d)
print(len(df))


gh_api = scraper.GitHubAPI("INSERT TOKENS") #test the scraper works

#traverse each slug
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
    ####################

    #### convert date of last commit from string ("2015-01") to integer (201501)
    st = df['lastCommit'][i]
    if i == 0:
        datePeak = int(st[0:4] + st[5:7])
    if isinstance(st, type(str)):
        datePeak = int(st[0:4] + st[5:7])
    ####
    
    #### get historical timeline of top 100 contributors
    problem = True
    try:
        d = pd.DataFrame(gh_api.repo_contributors(s)).set_index('user')
        d.columns = pd.to_datetime(d.columns, unit='s')
        problem = False
    except:
        pass
    if problem == True: 
        df['contributorsToLastComm'][i] = 0
        continue
    #### 
     
    count = 0
    k = 0
    #### ignore contributors who came before 2015-01 (our date of collection)
    while int(d.columns[k].strftime('%Y-%m')[0:4] + d.columns[k].strftime('%Y-%m')[5:7]) < 201501:
        k += 1
    kk = k
    
    ### if count is greater than 0 / ever increments above 1, there was at least one contributor before the project crashed
    while int(d.columns[k].strftime('%Y-%m')[0:4] + d.columns[k].strftime('%Y-%m')[5:7]) < datePeak:
        count += 1
        k+=1
    
    ### if count == 0, there were no contributors, so set the variable to 0 and continue
    if count==0:
        df['contributorsToLastComm'][i] = 0
        continue
        
    ### else count the total number of contributors 
    d = d.iloc[:, kk:(kk+count)]
    totalContributors = 0
    for k in range(0, len(d)):
        if d.sum(axis=1)[k] > 0:
            totalContributors+=1

    df['contributorsToLastComm'][i] = totalContributors
    df.to_csv("pydrillerCommits.csv")
    if i%100==0:
        print(str(i) + ", total contributors: "+str(df['contributorsToLastComm'][i]))
