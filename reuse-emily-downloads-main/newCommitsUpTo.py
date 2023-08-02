# from datetime import date, time
# import requests
# from prometheus_client import start_http_server, Summary, Counter
# from pydriller.repository import Repository  
# from pydriller.metrics.process.commits_count import CommitsCount
# import pydriller # Pydriller is the library we use to go through the commits on disc 
# from git import Repo, Commit
# import csv
# import os
# import pandas as pd
# import numpy as np
# from builtins import any as b_any
# import stscraper as scraper
# import warnings
# warnings.filterwarnings("ignore")
# from dateutil.relativedelta import relativedelta
# import mysql.connector
# mydb = mysql.connector.connect(
#   user="emilyngu",
#   password="",
#   host="localhost",
#   port =3306)

# mycursor = mydb.cursor()

# os.chdir("/data3/emilyngu")
# #df = pd.read_csv("errors.csv")
# df = pd.read_csv("new99.csv")
# print(len(df))

# jan15start = date(2015,1,1)
# dec20end = date(2020,12,1)
# startTime = time(7,00,00)
# endTime = time(19,00,00)

# monthStart_dates = {}
# yearMonth_names = {}
# for year in range (2015, 2021):
#     for month in range(1, 13):
#         monthidx = (year-2015)*12+month-1
#         monthStart_dates[monthidx] = date(year, month, 1)
#         yearMonth_names[monthidx] = f"{year}-{month}"


# def getmonthidx(date):
#             # checks to make sure commit is within 2015-jan - 2020-dec date range
#             if date >= jan15start and date <= dec20end:
#                 # determines month index for date
#                 for monthidx in range(0, len(monthStart_dates)):
#                     #checks to make sure it won't be out of range
#                     if monthidx + 1 < len(monthStart_dates):
#                         if date < monthStart_dates[monthidx + 1]:
#                             return monthidx
#                     # if this is true then its dec-20 and that is the monthindex that should be returned
#                     elif monthidx + 1 >= len(monthStart_dates):
#                         return monthidx
#             return -1

# count = 0
# for i in range(0, len(df)):
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
#     try:
#         if s.find('/')!=-1:
#             st = s.replace(s[s.find('/')], '_____')
#     except:
#         pass
#     if df['peakIndex'][i]!=-1:
#         peakIndex = df['peakIndex'][i]
#     a = "/data3/emilyngu/" + st

#     try:
#         qu = "SELECT yearMonth, numCommits FROM emily.emily_marxist_NPMImportant120kMonthlySlugAggregates WHERE slug = '"+df['slug'][i]+"';"
    
#         mycursor.execute(qu)

#         myresult = mycursor.fetchall()
#         myresult = pd.DataFrame(myresult)
#         myresult.columns = ['yearMonth', 'numCommits']
#         totalCommitsSql = sum(myresult['numCommits'])
#         totalCommits = 0
#         jan15start = date(2015,1,1)
#         dec20end = date(2020,12,1)  
#         for commit in Repository(a).traverse_commits():
#             if getmonthidx(commit.author_date.date()) != -1:
#                 totalCommits += 1

#         if (totalCommits > 40 and (totalCommitsSql < (0.60)*totalCommits or totalCommitsSql > (1.4)*totalCommits)) or (totalCommitsSql==0 and totalCommits!=0) or df['monSinceLastComm'][i] >= 40:
#             print(df['slug'][i] + ", totalPythonCommits: " + str(totalCommits)+", sqlCommits: "+str(totalCommitsSql))
#             one = int(myresult['yearMonth'][peakIndex-1][0:4])
#             two = int(myresult['yearMonth'][peakIndex-1][5:7])
#             dec20end = date(one,two,1)
#             jan15start = date(2015,1,1)
#             monthsSinceLastCommit = 0
#             counter = 0
#             for commit in Repository(a).traverse_commits():
#                 if getmonthidx(commit.author_date.date()) != -1:
#                     if jan15start < dec20end:
#                         jan15start  = jan15start + relativedelta(months = 1)
#                         counter += 1
#                     else:
#                         break

#             if counter > 0:
#                 monthsSinceLastCommit = peakIndex +1 - counter

#             df['monSinceLastComm'][i] = monthsSinceLastCommit

#     except:
#         count += 1
#         print(df['slug'][i]+" " +str(count))
#         pass
#     df['hi'][i] = -1
#     df.to_csv("new99Commits.csv")
#     if i%500==0:
#         print(i)

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
from builtins import any as b_any
import stscraper as scraper
import warnings
warnings.filterwarnings("ignore")
from dateutil.relativedelta import relativedelta
import mysql.connector
mydb = mysql.connector.connect(
  user="emilyngu",
  password="",
  host="localhost",
  port =3306)

mycursor = mydb.cursor()

os.chdir("/data3/emilyngu")
# a list of unique slugs
df = pd.read_csv("pydrillerCommitsR.csv")
print(len(df))

jan15start = date(2015,1,1)
dec20end = date(2020,12,1)
startTime = time(7,00,00)
endTime = time(19,00,00)

monthStart_dates = {}
yearMonth_names = {}
for year in range (2015, 2021):
    for month in range(1, 13):
        monthidx = (year-2015)*12+month-1
        monthStart_dates[monthidx] = date(year, month, 1)
        yearMonth_names[monthidx] = f"{year}-{month}"


def getmonthidx(date):
            # checks to make sure commit is within 2015-jan - 2020-dec date range
            if date >= jan15start and date <= dec20end:
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

# traverse each slug
for i in range(0, len(df)):
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

    #get path to repo on disc
    a = "/data3/emilyngu/" + st


    # ignore this for now: at first I was trying to find the umbre of commits up to a certain date
    if df['peakIndex'][i]!=-1:
        peakIndex = df['peakIndex'][i]

    try:
        # run SQL query to get long-formatted, time-series commits over time for a certain slug in the list
        qu = "SELECT yearMonth, numCommitsWithDups FROM emily.emily_marxist_NPMImportant120kMonthlySlugAggregates_copy WHERE slug = '"+df['slug'][i]+"';"

        mycursor.execute(qu)

        ### myresult holds a dataframe of columns "yearMontH" and "numCommitsWithDups"
        myresult = mycursor.fetchall()
        myresult = pd.DataFrame(myresult)
        myresult.columns = ['yearMonth', 'numCommitsWithDups']


        totalCommitsSql = sum(myresult['numCommitsWithDups'])
        #if totalCommitsSql == 0:
        jan15start = date(2015,1,1)
        dec20end = date(2020,12,1) 

        # traverse each commit 
        for commit in Repository(a).traverse_commits():
            #must be between 2015-01 and 2020-12
            if getmonthidx(commit.author_date.date()) != -1:
                #get date of the commit
                dat = commit.author_date.date()
                # if month is less than 10, like March, set yearMonth to appear like "2015-03" by adding a "0" in front of the "3". truncate the day
                if dat.month <10:
                    s= str(dat.year) + "-0" + str(dat.month)
                else: # if month is >= 10, like November, don't add a "0" in front of them month nuumber and just write something like "2015-11". truncate the day
                    s= str(dat.year) + "-" + str(dat.month)

                #arr holds the index of myresult that is equal to that date of the commit
                arr = np.where(myresult['yearMonth'] == s)
                #increment the number of commits of the index of result we found
                if len(arr) > 0 and len(arr[0]) > 0:
                    myresult['numCommitsWithDups'][arr[0][0]] += 1

        #update date we saved in "result" into the SQL table
        for j in range(0, len(myresult)):
            qu = "update emily.marxist_NPMImportant120kMonthlySlugAggregates_copy_copy set numCommitsWithDups =" + str(myresult['numCommitsWithDups'][j]) + " where slug = '"+df['slug'][i]+"' and yearMonth = '" + str(myresult['yearMonth'][j]) + "';"
            mycursor.execute(qu)
            mydb.commit()

        #print(df['slug'][i] + ", totalPythonCommits: " + str(totalCommits)+", sqlCommits: "+str(totalCommitsSql))

        # if (totalCommits > 40 and (totalCommitsSql < (0.60)*totalCommits or totalCommitsSql > (1.4)*totalCommits)) or (totalCommitsSql==0 and totalCommits!=0) or df['monSinceLastComm'][i] >= 40:
        #     print(df['slug'][i] + ", totalPythonCommits: " + str(totalCommits)+", sqlCommits: "+str(totalCommitsSql))
        #     one = int(myresult['yearMonth'][peakIndex-1][0:4])
        #     two = int(myresult['yearMonth'][peakIndex-1][5:7])
        #     dec20end = date(one,two,1)
        #     jan15start = date(2015,1,1)
        #     monthsSinceLastCommit = 0
        #     counter = 0
        #     for commit in Repository(a).traverse_commits():
        #         if getmonthidx(commit.author_date.date()) != -1:
        #             if jan15start < dec20end:
        #                 jan15start  = jan15start + relativedelta(months = 1)
        #                 counter += 1
        #             else:
        #                 break

        #     if counter > 0:
        #         monthsSinceLastCommit = peakIndex +1 - counter

        #     df['monSinceLastComm'][i] = monthsSinceLastCommit

    except:
        print(df['slug'][i] + ", " + str(i))
        pass
    #     count += 1
    #     print(df['slug'][i]+" " +str(count))
    #     pass
    df.to_csv("pydrillerCommitsAll.csv")
    if i%100==0:
        print(i)
