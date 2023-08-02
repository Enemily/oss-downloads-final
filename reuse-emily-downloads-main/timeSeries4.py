import pandas as pd
import numpy as np
from sklearn import preprocessing 
from sklearn.metrics import mean_squared_log_error
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance
from matplotlib import pyplot as plt
import os
os.chdir("/data3/emilyngu")

#result2.csv holds long-formatted time series data on downloads, versions, commits, and opened/closed issues of 14,196 slugs. read it in and convert it to a dataframe
d = pd.read_csv("result2.csv")
melt = pd.DataFrame(d)

#big will hold the real download values from 2015/05 - 2019/12 PLUS the predicted download values from 2020/01 - 2020/12 for each project. bigActual will hold the real download values from 2015/05-2020/12 for each project. so for now just initialize each row to -1 and we'll replace it later
big = pd.DataFrame()
bigActual = pd.DataFrame()

#we'll divide the bulk predictions into groups, assigning each project to a group depending on the date of their last commit. datesAll: 201505 represents 2015-05
datesAll = [201505, 201506, 201507, 201508, 201509, 201510, 201511, 201511, 201512, 201601, 201602, 201603, 201604, 201605, 201606, 201607, 201608, 201609, 201610, 201611, 201611, 201612, 201701, 201702, 201703, 201704, 201705, 201706, 201707, 201708, 201709, 201710, 201711, 201711, 201712, 201801, 201802, 201803, 201804, 201805, 201806, 201807, 201808, 201809, 201810, 201811, 201811, 201812, 201601, 201902, 201903, 201904, 201905, 201906, 201907, 201908, 201909, 201910, 201911, 201911, 201912, 202001, 202002, 202003, 202004, 202005, 202006, 202007, 202008,202009, 202010, 202011, 202012]
datesAll = pd.DataFrame(datesAll)
datesAll.rename(columns={ datesAll.columns[0]: "date" }, inplace = True)

# function to calculate the error in the model's prediction
def rmsle(ytrue, ypred):
    return np.sqrt(mean_squared_log_error(ytrue, ypred))

# divide the bulk prediction into groups. each iteration of this for loops makes a bulk prediction only on projects who had their last commit in 2015-05, then 2015-06, then 2015-07,... ,2020-12
for i in range(0, len(datesAll)):
    print("STARTING NEW DATE: "+str(datesAll['date'][i]))

    print("about to subset data with same last commit")
    melt4 = melt[melt['lastCommit2']==datesAll['date'][i]]
    
    #DON'T TRY TO UNDERSTAND THIS: we basically assign id numbers to the projects
    print("about to call preprocessing label encoder")
    lbl = preprocessing.LabelEncoder() 
    lbl.fit(melt4['slug'])
    melt4['slug'] = lbl.transform(melt4['slug'])
    print("about to sort values by yearMonth2 and slug")
    melt4 = melt4.sort_values(['yearMonth2', 'slug'])
    print("about to rename id columns")
    melt4 = melt4.rename({'id': 'ID'}, axis=1)
    #melt4 = melt4.drop('ID', axis=1)
    melt4 = melt4.rename({'slug': 'id'}, axis=1)
    
    # create the lag variables (1)downloads from last month before 2020/12 (2) downloads from last last month before 2020/12 (3) downlaods from last last last month before 2020/12, etc.
    print("sorting last week downloads")
    melt4['Last_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift()
    melt4['Last_Week_Diff'] = melt4.groupby(['id'])['Last_Week_Downloads'].diff()
    melt4['Last-1_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(2)
    melt4['Last-1_Week_Diff'] = melt4.groupby(['id'])['Last-1_Week_Downloads'].diff()
    melt4['Last-2_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(3)
    melt4['Last-2_Week_Diff'] = melt4.groupby(['id'])['Last-2_Week_Downloads'].diff()
# create more lag variables (1)commits from last month before 2020/12 (2) commits from last last month before 2020/12 (3) commits from last last last month before 2020/12, etc.
    print("sorting last week commits")
    melt4['Last_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift()
    melt4['Last_Week_Diff_Commits'] = melt4.groupby(['id'])['Last_Week_Commits'].diff()
    melt4['Last-1_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(2)
    melt4['Last-1_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-1_Week_Commits'].diff()
    melt4['Last-2_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(3)
    melt4['Last-2_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-2_Week_Commits'].diff()

# create more lag variables (1)versions from last month before 2020/12 (2) versions from last last month before 2020/12 (3) versions from last last last month before 2020/12, etc.
    print("sorting last week versions")
    melt4['Last_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift()
    melt4['Last_Week_Diff_Versions'] = melt4.groupby(['id'])['Last_Week_Versions'].diff()
    melt4['Last-1_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(2)
    melt4['Last-1_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-1_Week_Versions'].diff()
    melt4['Last-2_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(3)
    melt4['Last-2_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-2_Week_Versions'].diff()

# create more lag variables (1)issues opened from last month before 2020/12 (2) issues opened from last last month before 2020/12 (3) issues opened from last last last month before 2020/12, etc.
    print("sorting last week opened issues")
    melt4['Last_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift()
    melt4['Last_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last_Week_IssuesOpened2'].diff()
    melt4['Last-1_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(2)
    melt4['Last-1_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-1_Week_IssuesOpened2'].diff()
    melt4['Last-2_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(3)
    melt4['Last-2_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-2_Week_IssuesOpened2'].diff()

# create more lag variables (1)issues closed from last month before 2020/12 (2) issues closed from last last month before 2020/12 (3) issues closed from last last last month before 2020/12, etc.
    print("sorting last week closed issues")
    melt4['Last_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift()
    melt4['Last_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last_Week_IssuesClosed2'].diff()
    melt4['Last-1_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(2)
    melt4['Last-1_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-1_Week_IssuesClosed2'].diff()
    melt4['Last-2_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(3)
    melt4['Last-2_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-2_Week_IssuesClosed2'].diff()

#get rid of ugly unimportant columns from the training data that we don't need
    melt4 = melt4.drop(['numIssuesOpened2', 'numIssuesClosed2', 'numCommitsWithDups', 'numVersions'], axis = 1)
    melt4 = melt4.dropna()
    

##########DON'T TRY TO UNDERSTAND THIS: just does some data arranging into the dataframes "d" and "dActual"
    print("about to subset datesAll and datesBefore")
    datesBefore = datesAll[datesAll['date']<=datesAll['date'][i]].date.tolist()
    datesAfter = datesAll[datesAll['date']>datesAll['date'][i]].date.tolist()
    
    #create some dataframes to store the predictions in
    d = pd.DataFrame()
    dActual = pd.DataFrame()
    
    print("starting for date in datesBefore loop")
    for date in datesBefore:
        
        ss = str(date)
        thing = melt4[melt4['yearMonth2'] == date]

        if len(thing)!=len(d) and datesBefore[0]!=date:
            print("HELLO")
            d[ss] = thingy.tolist()
            dActual[ss] = thingy.tolist()
            continue

        thingy = thing['numDownloads'].values
        #print(str(datesAll['date'][i])+" "+ss + " "+str(len(thingy)) + " "+str(len(d)))
        d[ss] = thingy.tolist()
        dActual[ss] = thingy.tolist()
        #s = ss + "_ID"
        dActual['ID'] = thing['ID'].values.tolist()
        #d[s] = thing['ID'].values.tolist()
    
    print("starting  for date in datesAfter loop")
    for date in datesAfter:
        ss = str(date)
        thing = melt4[melt4['yearMonth2'] == date]

        if len(thing)!=len(d):
            d[ss] = thingy.tolist()
            dActual[ss] = thingy.tolist()
            continue
        
        thingy = thing['numDownloads'].values
        #print(str(datesAll['date'][i])+" "+ss + " "+str(len(thingy)) + " "+str(len(d)))
        dActual[ss] = thingy.tolist()
        #s = ss + "_ID"
        dActual['ID'] = thing['ID'].values.tolist()

    bigActual = pd.concat([bigActual, dActual])

    dates = melt4[melt4['yearMonth2'] > datesAll['date'][i]].yearMonth2.tolist()
    dates=sorted(set(dates))
####################DON'T TRY TO UNDERSTAND ABOVE:



   #this for loop predicts the downloads of all projects for month of last commit m, m+1, m+2, all the way up to 2020-12. So, each iteration reprents a month we're trying to predict
    mean_error = []
    print("start big main for loop")
    for date in dates:
    
    ######DON'T TRY TO UNDERSTAND: just deals with minor errors
        s = str(date)
        if dates[0] == 201510 and date == 201510:
            # thing = melt4[melt4['yearMonth2'] == 201509]
            # thingy = thing['numDownloads'].values
            d[s] = dActual[s]
            continue
        if dates[0] == 201604 and date == 201604:
            d[s] = dActual[s]
            continue

        if date == 201510:
            if len(d)!=len(p):
                d[s] = dActual[s]
            else:
                d[s] = p.tolist()
            continue
        if date == 201604:
            if len(d)!=len(p):
                d[s] = dActual[s]
            else:
                d[s] = p.tolist()
            continue
    #######DON'T TRY TO UNDERSTAND ABOVE
    
        #try:
   
        train = melt4[melt4['yearMonth2'] < date] #training data (all data coming before date of last commit)
        #if len(val) != len(thingg)
        val = melt4[melt4['yearMonth2'] == date] #testing data (data during month of last commit)
        
        # get rid of the variables we don't need for the prediction
        xtr, xts = train.drop(['numDownloads', 'id', 'yearMonth2', 'lastCommit2', 'ID'], axis=1), val.drop(['numDownloads', 'id', 'yearMonth2', 'lastCommit2', 'ID'], axis=1)
       
       # get a hold of the downloads we're actually trying to predict
        ytr, yts = train['numDownloads'].values, val['numDownloads'].values
        
        #run it through the random forest/gradient boosted model (use 100 trees and a learning rate of 0.05)
        mdl = LGBMRegressor(n_estimators=100, learning_rate=0.05)
        mdl.fit(xtr, np.log1p(ytr))
        p = np.expm1(mdl.predict(xts))     

        #DON'T TRY TO UNDERSTAND THIS: deals with minor errors
        if len(d)!=len(p):
            print("UNEVEN LEN(D) ["+str(len(d))+"] != LEN(P) ["+str(len(p))+"] in date of last commit: " + str(datesAll['date'][i])+" with prediction date: "+str(date))
            d[s]  =dActual[s]
            continue
        print("date of last commit: " + str(datesAll['date'][i]) +". date we predicted: "+s)

        d[s] = p.tolist()
        if len(val['ID'])!=len(dActual['ID']):
            print("UNEQUAl val['ID'] ["+str(len(val['ID']))+"] != dActual['ID'] ["+str(len(dActual['ID']))+"]  in date of last commit: " + str(datesAll['date'][i])+" with prediction date: "+str(date))
            continue
        if len(val['ID'])==len(p):
            d['ID'] = val['ID'].values.tolist()
        else:
            d['ID'] = dActual['ID']
        #DON'T TRY TO UNDERSTAND ABOVE: deals with minor errors
            
        # calculate the model's error
        error = rmsle(yts, p)
        mean_error.append(error) #add to an array to calculate the average error for all testing years at the end

    #DON'T TRY TO UNDERSTAND: deals w minor errors
    try:
        if len(d)==len(val['ID']):
            d['ID'] = val['ID'].values.tolist()
        else:
            d['ID'] = dActual['ID']
    #DON'T TRY TO UNDERSTAND ABOVE: deals with minor errors
    except:
        pass
    
    #put the predictions into a dataframe
    big = pd.concat([big, d])
    big.to_csv("big.csv")
    bigActual.to_csv("bigActual.csv")
print("this is a prediciton with test data after the last commit for ordered id ranges 1-14000")
