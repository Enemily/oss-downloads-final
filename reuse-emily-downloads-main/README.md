# We mainly ran three models (with some variations to them) that predict whether or not projects "die" (crash, peak, etc.).
- our general definition of whether a project "died" / "peaked" is: a downward trend in its downloads over time
- the models are Survival Analysis (specifically Cox Proportional Hazards model), Logistic Regression, and time series forecasting (specifically a Gradient Boosted model that "globally" predicts downloads for all 30k projects at once)
- also attached are other scripts of how I collected the data to run these 3 models on
- also attached are scripts that run some data visualizations of downloads over time

# Short description of each script:

# Survival Analysis.Rmd: this script runs the survival model with the survival outcome being whether or not the project "peaked"
- for this script, we determine whether the project "peaked" if it had less than 0.5x the number of downloads 3 years later at some point (between 2015-2020)
- MODEL PREDICTORS:
  - number of downloads, commits, and versions

# logit.R: this script runs the logistic regression model that predicts whether or not projects crash ("peak") depending on some predictors
- predictors: 
  - archivedOrDepr (true/false)
  - number months since last opened issue up until the project peaked
  - number months since last commit or closed issue (whichever is most recent) up until the project peaked
  - number commits up until project peaked
  - number opened issues up until project peaked
  - number versions up until project peaked
  - number downloads at peak
  - project age up to peak
  - project size
  - contributors up to the peak
- response: if the project "peaked" or not (true/false) (the binary response variable is called "peakFitted" and it's explained further in the noUglySlugs.csv section of this README)

# timeSeries3.py: this script runs the "Global" Time Series Model
- forecasts the number of downloads of 15k separate GitHub projects at once using a Gradient Boosting model
- training date range: [2019/09 to 2019/12]
- testing date range: [2020/01 to 2020/12]
- MODEL PREDICTORS: 
  - we make a prediction for each month in the testing range. So for each month, select the top 20 most important predictors listed below (do this by analyzing the "feature importance" of each predictor) to use for the model and run the model on that month. Repeat this process for all the other testing months
  - number downloads 1 month ago
    - and the monthly differences/"first derivates" in # downloads 1 month ago
      - for example: numDownloadsOneMonthAgo at time t - numDownloadsOneMonthAgo at time t-1
  - number downloads 2 months ago
    - and the monthly differences/"first derivates" in # downloads 2 months ago
    - for example: numDownloadsTwoMonthsAgo at time t - numDownloadsTwoMonthsAgo at time t-1
  - number downloads 3 months ago
    - and the monthly differences/"first derivates" in # downloads 3 months ago 
    - for example: numDownloadsThreeMonthshAgo at time t - numDownloadsThreeMonthsAgo at time t-1
  - number downloads 4 months ago
    - and the monthly differences/"first derivates" in # downloads 4 months ago 
    - for example: numDownloadsFourMonthsAgo at time t - numDownloadsFourMonthsAgo at time t-1
  - number downloads 5 months ago
    - and the monthly differences/"first derivates" in # downloads 5 months ago 
    - for example: numDownloadsFiveMonthsAgo at time t - numDownloadsFiveMonthsAgo at time t-1
  - number commits 1 month ago
    - and the monthly differences/"first derivates" in # commits 1 month ago
      - for example: numCommitsOneMonthAgo at time t - numCommitsOneMonthAgo at time t-1
  - number commits 2 months ago
    - and the monthly differences/"first derivates" in # commits 2 months ago
    - for example: numCommitsTwoMonthsAgo at time t - numCommitsTwoMonthsAgo at time t-1
  - number commits 3 months ago
    - and the monthly differences/"first derivates" in # commits 3 months ago 
    - for example: numCommitsThreeMonthshAgo at time t - numCommitsThreeMonthshAgo at time t-1
  - number commits 4 months ago
    - and the monthly differences/"first derivates" in # commits 4 months ago 
    - for example: numCommitsFourMonthsAgo at time t - numCommitsFourMonthsAgo at time t-1
  - number commits 5 months ago
    - and the monthly differences/"first derivates" in # downloads 5 months ago 
    - for example: numCommitsFiveMonthsAgo at time t - numCommitsFiveMonthsAgo at time t-1
  - number versions 1 month ago
    - and the monthly differences/"first derivates" in # versions 1 month ago
      - for example: numVersionsOneMonthAgo at time t - numVersionsOneMonthAgo at time t-1
  - number versions 2 months ago
    - and the monthly differences/"first derivates" in # versions 2 months ago
    - for example: numVersionsTwoMonthsAgo at time t - numVersionsTwoMonthsAgo at time t-1
  - number versions 3 months ago
    - and the monthly differences/"first derivates" in # versions 3 months ago 
    - for example: numVersionsThreeMonthshAgo at time t - numVersionsThreeMonthshAgo at time t-1
  - number versions 4 months ago
    - and the monthly differences/"first derivates" in # versions 4 months ago 
    - for example: numVersionsFourMonthsAgo at time t - numVersionsFourMonthsAgo at time t-1
  - number versions 5 months ago
    - and the monthly differences/"first derivates" in # versions 5 months ago 
    - for example: numVersionsFiveMonthsAgo at time t - numVersionsFiveMonthsAgo at time t-1
  - number issues opened 1 month ago
    - and the monthly differences/"first derivates" in # issues opened 1 month ago
      - for example: numOpenedIssuesOneMonthAgo at time t - numOpenedIssuesOneMonthAgo at time t-1
  - number issues opened 2 months ago
    - and the monthly differences/"first derivates" in # issues opened 2 months ago
    - for example: numOpenedIssuesTwoMonthsAgo at time t - numOpenedIssuesTwoMonthsAgo at time t-1
  - number issues opened 3 months ago
    - and the monthly differences/"first derivates" in # issues opened 3 months ago 
    - for example: numOpenedIssuesThreeMonthshAgo at time t - numOpenedIssuesThreeMonthshAgo at time t-1
  - number issues opened 4 months ago
    - and the monthly differences/"first derivates" in # issues opened 4 months ago 
    - for example: numOpenedIssuesFourMonthsAgo at time t - numOpenedIssuesFourMonthsAgo at time t-1
  - number issues opened 5 months ago
    - and the monthly differences/"first derivates" in # issues opened 5 months ago 
    - for example: numOpenedIssuesFiveMonthsAgo at time t - numOpenedIssuesFiveMonthsAgo at time t-1
  - number issues closed 1 month ago
    - and the monthly differences/"first derivates" in # issues closed 1 month ago
      - for example: numClosedIssuesOneMonthAgo at time t - numClosedIssuesOneMonthAgo at time t-1
  - number issues closed 2 months ago
    - and the monthly differences/"first derivates" in # issues closed 2 months ago
    - for example: numClosedIssuesTwoMonthsAgo at time t - numClosedIssuesTwoMonthsAgo at time t-1
  - number issues closed 3 months ago
    - and the monthly differences/"first derivates" in # issues closed 3 months ago 
    - for example: numClosedIssuesThreeMonthshAgo at time t - numClosedIssuesThreeMonthshAgo at time t-1
  - number issues closed 4 months ago
    - and the monthly differences/"first derivates" in # issues closed 4 months ago 
    - for example: numClosedIssuesFourMonthsAgo at time t - numClosedIssuesFourMonthsAgo at time t-1
  - number issues closed 5 months ago
    - and the monthly differences/"first derivates" in # issues closed 5 months ago 
    - for example: numClosedIssuesFiveMonthsAgo at time t - numClosedIssuesFiveMonthsAgo at time t-1
- MODEL RESPONSE: 
  - number of downloads predicted at each month between [2020/01 to 2020/12]

# timeSeries4.py: similar to timeSeries3.py, this script also runs a "Global" Time Series Model, but the training and testing dates differ
- forecasts the number of downloads of 15k separate GitHub projects at once using a Gradient Boosting model
- training date range: [2015/05 - month of the last commit of the project]
- testing date range: [month after the project's last commit - 2020/12]
- MODEL PREDICTORS: same as timeSeries3.py
- MODEL RESPONSE: # downloads predicted at each month after the project's last commit

# plots.Rmd: 
- this script plots number of downloads over time & number of commits over time for 100 random projects. 
- Data is from the SQL table emily.marxist_NPMImportant120kMonthlySlugA_pydriller_NoOutlier.

# findPeaked_one.R: 
- for each slug in our dataset, mark whether it "peaked" or not (true/false). 
- The slugs in our dataset are in noUglySlugs.csv, as described further below in this README.
- the definition of "peaked" is whether the maximum of the best fitted curve of a project's numDownloads-vs-time plot is not during the last month (2020/12) 
- if a project peaked, save the month it peaked

# findPeaked_two.R: 
- for each slug, mark whether it "peaked" or not (true/false)
- the definition of "peaked" is whether the best fitted curve of a project's numDownloads-vs-time plot has a downward slope that is steeper than some threshold value
- if a project peaked, save the month it peaked

# newCommitsUpTo.py:
- mine historical data on commits for each project in noUglySlugs.csv and save it into SQL table emily.marxist_NPMImportant120kMonthlySlugA_pydriller_NoOutlier

# contributorsUpToPeak.py: 
- for each slug, find the total # contributors before the project "peaked" 

# deprecated.py: 
- for each slug, look at their most recent commits and check whether terms like "deprecated," "abandoned," or "no longer maintainted" were added to their README file (true/false)

# deprecated2.py: 
- for each slug, look at whether terms like "deprecated," "abandoned," or "no longer maintainted" exist in the first few lines of their README file (true/false)

# archived.py: 
- for each slug, check whether the project was archived
- additionally, find the repo's total size in kilobytes and repo's total number of stars

# noUglySlugs.csv: this csv holds the data to do the Logistic Regression model (logit.Rmd) on
- rows are the different slugs, columns have info about each slug
  - columns collect the total counts of something up until the project peaked (we don't count data collected after the peak). If the project did not peak, the column collects total counts of something until the peak date of the most recent project that came before it in the table and actually peaked
- the table in SQL called emily.marxist_NPMImportant120kMonthlySlugA_pydriller_NoOutlier has historical/long-formatted data for each slug, with the number of downloads, opened/closed issues, versions, and commits at each year and month. I collected most of the variables in noUglySlugs.csv from that SQL table
  - certain variables (peakIndex, peakFitted, archived, starsUpTo, dead, and archivedOrDepr) were collected from the scripts findPeaked_one.Rmd, findPeaked_two.Rmd, archived.py, deprecated.py, deprecated2.py, and contributorsUpToPeak.py as discussed elsewhere in this README file
- VARIABLES
  - peakIndex: there are 72 months between 2015/01 - 2020/12 is 72. the peakIndex ranges from [0, 72] and keep tracks of the month when the project peaked. if a project didn't peak, set peakIndex to -1.
  - peaked: if the number of downloads at some month m is at least 2x greater than the number of downloads at m+24 (2 years later), set peaked to true.
  - issuesOpenedUpToPeak: total issues opened up until the project peaked
  - demandUpToPeak: if there were any issues opened before the project peaked
  - commitsUpToPeak: total commits made up until the project peaked
  - issuesClosedUpToPeak: total issues closed up until the project peaked
  - lastOpen: date of the last opened issue before the project peaked
  - lastClosed: date of the last closed issue before the project peaked
  - lastCommit: date of the last commit before the project peaked
  - downloadsUpTo: total number downloads up until the project peaked
  - archived: if the project was archived or not
  - starsUpTo: total stars of the project (before and after it peaked)
  - versionsUpTo: total number of versions released up until the project peaked
  - age: number of months from 2015/01 up until the project peaked
  - dead: if words like "deprecated" "abandoned" "no longer maintained" exist in the project's readme
  - dateOfPeak: date of when the project peaked
  - size: total size of the project in kilobytes as of now
  - downloadsAtPeak: number of downloads during the month the proejct peaked
  - monSinceLastOpIssue: # months between the time of last opened issue before the peak and the peak
  - monSinceLastCommOrClosedIssue: # months between the time of last closed issue or commit before the peak (whichever occured later) and the peak
  - monSinceLastComm: # months between the time of last commit before the peak and the peak
  - monSinceLastClosedIssue: # months between the time of last closed issue before the peak and the peak
  - contributorsToLastComm: total # contributors up until the project peaked
  - archivedOrDepr: if the project was archived or words like "deprecated" "abandoned" or "no longer maintained" were in the readmefile, set archivedOrDepr to true
  - peakFitted: if the maximum of the fitted curve of the project's downloads-vs-time plot does not occur within the last month (2020/12), set to true

# Data Visualizations: 
- randomForest.html: plotted output of timeSeries3.py
  - real values are in black, predictions in red (predictions were made only in the last year)
- RFLastCommit.html: plotted output of tiemSeries4.py
  - real values are in black, predictions in red (predictions were made only after the project's last commit)
- box plot scaled.Rmd: box plot time series of downloads over time 
  - did this for projects that crashed and didn't crash

# miscellaneous csv files that some of the scripts use
- big.csv: time series forecasts of downloads of every project 
- bigActual.csv: time series of downloads (original values) of every project 
- query_result.csv: time series downloads, commits, versions, opened issues, and closed issues (original values) of every project
- random100.csv: list of 100 random slugs
- new99.csv: list of slugs used in the Survival Analysis.Rmd model script
- * other scripts are not directly linked here but they are located in the tardigrade database /data3/emilyngu

