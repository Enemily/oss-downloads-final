import pandas as pd
import numpy as np
import os
from sklearn import preprocessing 
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_log_error
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
os.chdir("/data3/emilyngu")

#result2.csv holds long-formatted time series data on downloads, versions, commits, and opened/closed issues of 14,196 slugs. read it in and convert it to a dataframe
d = pd.read_csv("result2.csv")
melt = pd.DataFrame(d)

#d will hold the real download values from 2015/05 - 2019/12 PLUS the predicted download values from 2020/01 - 2020/12 for each project. dActual will hold the real download values from 2015/05-2020/12 for each project. so for now just initialize each row to -1 and we'll replace it later
d = pd.DataFrame([-1]*14196)
dActual = d
#this model forecasts the downloads using many predictors, not just past downloads: past downloads, commits, versions, opened/closed issues. There are 14196 projects and they each have a unique id number
print("This uses all predictors with id in order from 1 to 14000")

#get rid of weird ugly columns read in from result2.csv
melt = melt.drop('slug', axis = 1)
melt = melt.drop('lastCommit2', axis = 1)

#convert data to wide format
melt = melt.sort_values(['yearMonth2', 'id'])

# create the lag variables (1)downloads from last month before 2020/12 (2) downloads from last last month before 2020/12 (3) downlaods from last last last month before 2020/12, etc.
melt4 = melt.copy()
melt4['Last_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift()
melt4['Last_Week_Diff'] = melt4.groupby(['id'])['Last_Week_Downloads'].diff()
melt4['Last-1_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(2)
melt4['Last-1_Week_Diff'] = melt4.groupby(['id'])['Last-1_Week_Downloads'].diff()
melt4['Last-2_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(3)
melt4['Last-2_Week_Diff'] = melt4.groupby(['id'])['Last-2_Week_Downloads'].diff()
melt4['Last-3_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(4)
melt4['Last-3_Week_Diff'] = melt4.groupby(['id'])['Last-3_Week_Downloads'].diff()
melt4['Last-4_Week_Downloads'] = melt4.groupby(['id'])['numDownloads'].shift(5)
melt4['Last-4_Week_Diff'] = melt4.groupby(['id'])['Last-4_Week_Downloads'].diff()

# create more lag variables (1)commits from last month before 2020/12 (2) commits from last last month before 2020/12 (3) commits from last last last month before 2020/12, etc.
melt4['Last_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift()
melt4['Last_Week_Diff_Commits'] = melt4.groupby(['id'])['Last_Week_Commits'].diff()
melt4['Last-1_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(2)
melt4['Last-1_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-1_Week_Commits'].diff()
melt4['Last-2_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(3)
melt4['Last-2_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-2_Week_Commits'].diff()
melt4['Last-3_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(4)
melt4['Last-3_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-3_Week_Commits'].diff()
melt4['Last-4_Week_Commits'] = melt4.groupby(['id'])['numCommitsWithDups'].shift(5)
melt4['Last-4_Week_Diff_Commits'] = melt4.groupby(['id'])['Last-4_Week_Commits'].diff()

# create more lag variables (1)versions from last month before 2020/12 (2) versions from last last month before 2020/12 (3) versions from last last last month before 2020/12, etc.
melt4['Last_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift()
melt4['Last_Week_Diff_Versions'] = melt4.groupby(['id'])['Last_Week_Versions'].diff()
melt4['Last-1_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(2)
melt4['Last-1_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-1_Week_Versions'].diff()
melt4['Last-2_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(3)
melt4['Last-2_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-2_Week_Versions'].diff()
melt4['Last-3_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(4)
melt4['Last-3_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-3_Week_Versions'].diff()
melt4['Last-4_Week_Versions'] = melt4.groupby(['id'])['numVersions'].shift(5)
melt4['Last-4_Week_Diff_Versions'] = melt4.groupby(['id'])['Last-4_Week_Versions'].diff()

# create more lag variables (1)issues opened from last month before 2020/12 (2) issues opened from last last month before 2020/12 (3) issues opened from last last last month before 2020/12, etc.
melt4['Last_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift()
melt4['Last_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last_Week_IssuesOpened2'].diff()
melt4['Last-1_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(2)
melt4['Last-1_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-1_Week_IssuesOpened2'].diff()
melt4['Last-2_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(3)
melt4['Last-2_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-2_Week_IssuesOpened2'].diff()
melt4['Last-3_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(4)
melt4['Last-3_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-3_Week_IssuesOpened2'].diff()
melt4['Last-4_Week_IssuesOpened2'] = melt4.groupby(['id'])['numIssuesOpened2'].shift(5)
melt4['Last-4_Week_Diff_IssuesOpened2'] = melt4.groupby(['id'])['Last-4_Week_IssuesOpened2'].diff()

# create more lag variables (1)issues closed from last month before 2020/12 (2) issues closed from last last month before 2020/12 (3) issues closed from last last last month before 2020/12, etc.
melt4['Last_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift()
melt4['Last_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last_Week_IssuesClosed2'].diff()
melt4['Last-1_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(2)
melt4['Last-1_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-1_Week_IssuesClosed2'].diff()
melt4['Last-2_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(3)
melt4['Last-2_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-2_Week_IssuesClosed2'].diff()
melt4['Last-3_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(4)
melt4['Last-3_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-3_Week_IssuesClosed2'].diff()
melt4['Last-4_Week_IssuesClosed2'] = melt4.groupby(['id'])['numIssuesClosed2'].shift(5)
melt4['Last-4_Week_Diff_IssuesClosed2'] = melt4.groupby(['id'])['Last-4_Week_IssuesClosed2'].diff()
melt4 = melt4.dropna()

#dates is the testing dataset: 2020-01 to 2020-12
dates = [202001, 202002, 202003, 202004, 202005, 202006, 202007, 202008,202009, 202010, 202011, 202012]
#datesBefore is the training dataset: 2015-07 to 2020-12
datesBefore = [201507, 201508, 201509, 201510, 201511, 201511, 201512, 201601, 201602, 201603, 201604, 201605, 201606, 201607, 201608, 201609, 201610, 201611, 201611, 201612, 201701, 201702, 201703, 201704, 201705, 201706, 201707, 201708, 201709, 201710, 201711, 201711, 201712, 201801, 201802, 201803, 201804, 201805, 201806, 201807, 201808, 201809, 201810, 201811, 201811, 201812, 201601, 201902, 201903, 201904, 201905, 201906, 201907, 201908, 201909, 201910, 201911, 201911, 201912]

# function to calculate the error in the model's prediction
def rmsle(ytrue, ypred):
    return np.sqrt(mean_squared_log_error(ytrue, ypred))

#DON'T TRY TO UNDERSTAND: this is just the messy part that fills the dataframes "d" and 'dActual" with real values of downloads from 2015-05 to 2019-12 before we make the prediction
for dateBefore in datesBefore:
    ss = str(dateBefore)
    thing = melt4[melt4['yearMonth2'] == dateBefore]
    if len(thing)!=len(d) and dateBefore!=201507:
        d[ss] = thingy.tolist()
        dActual[ss] = thingy.tolist()
        print("This date doesn't exist for all slugs: " + ss)
        continue
    thingy = thing['numDownloads'].values
    d[ss] = thingy.tolist()
    dActual[ss] = thingy.tolist()


#DON'T TRY TO UNDERSTAND: this is just the messy part that fills the dataframes "d" and 'dActual" with real values of downloads from 2015-05 to 2019-12 before we make the prediction
for date in dates:
    ss = str(date)
    thing = melt4[melt4['yearMonth2'] == date]
    if len(thing)!=len(d):
        dActual[ss] = thingy.tolist()
        print("This date doesn't exist for all slugs: " + ss)
        continue
    thingy = thing['numDownloads'].values
    dActual[ss] = thingy.tolist()
dActual.to_csv("timeSeries5Actual.csv")


#this for loop predicts the downloads of all projects for month 2020-01, then 2020-02, them 2020-03, ..., then 2020-12. So, each iteration reprents a month we're trying to predict
mean_error = []
for date in dates:
    print("starting this date now: " + str(date))
    try:
        train = melt4[melt4['yearMonth2'] < date] #training data
        val = melt4[melt4['yearMonth2'] == date] #testing data for month "date"
        
        # get rid of the variables we don't need for the prediction
        xtr, xts = train.drop(['numDownloads', 'id', 'yearMonth2', 'numIssuesOpened2', 'numIssuesClosed2', 'numCommitsWithDups', 'numVersions'], axis=1), val.drop(['numDownloads', 'id', 'yearMonth2', 'numIssuesOpened2', 'numIssuesClosed2', 'numCommitsWithDups', 'numVersions'], axis=1)
        
        # get a hold of the downloads we're actually trying to predict
        ytr, yts = train['numDownloads'].values, val['numDownloads'].values
        
        #run it through the random forest/gradient boosted model (use 100 trees and a learning rate of 0.05)
        mdl = LGBMRegressor(n_estimators=100, learning_rate=0.1)
        mdl.fit(xtr, np.log1p(ytr))

        #FEATURE IMPORTANCE PART: find the top 20 most important predictors and rerun the model with them only
        importances = pd.DataFrame(data={
        'Attribute': xtr.columns,
        'Importance': mdl.feature_importances_
        })
        importances = importances.sort_values(by='Importance', ascending=False)
        importances=importances[0:20]
        importances = importances.reset_index(drop=True)
        importances = importances.T
        importances.columns = importances.iloc[0]
        importances = importances[1:]
        xtr = xtr[xtr.columns & importances.columns]
        xts = xts[xts.columns & importances.columns]

        #as mentioned, rerun the model now with the 20 most important predictors only
        mdl = LGBMRegressor(n_estimators=100, learning_rate=0.1)
        mdl.fit(xtr, np.log1p(ytr))

        p = np.expm1(mdl.predict(xts))
        s = str(date)

        # #PLOT FEATURE IMPORTANCE
        # importances = pd.DataFrame(data={
        # 'Attribute': xtr.columns,
        # 'Importance': mdl.feature_importances_
        # })
        # importances = importances.sort_values(by='Importance', ascending=False)

        # plt.bar(x=importances['Attribute'], height=importances['Importance'], color='#087E8B')
        # plt.title('Feature importances obtained from coefficients', size=20)
        # plt.xticks(rotation='vertical')
        # plt.show()
        
        # save the prediction to our ultimate dataframe, d, that holds the predictions for all testing years
        d[s] = p.tolist()
        
        # calcualte the model's error
        error = rmsle(yts, p)
        print("This date worked! Error: " + str(error))
        mean_error.append(error) #add to an array to calculate the average error for all testing years at the end
        d.to_csv("timeSeries5.csv")
    except:
        print("didn't work: " + str(date))
print("This is a prediction based on the top 20 important predictors and with ordered id 1-14000 . Mean error: ")
print(np.mean(mean_error))
