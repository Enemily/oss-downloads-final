#what this script does is for each slug, find if the project "peaked" or not and mark if so in a boolean variable called peakFitted
library(ggplot2)
library(ggpubr)
library(RMySQL)
mydb = dbConnect(MySQL(), user = "emilyngu", password = "", dbname = "emily", host = "127.0.0.1")

setwd("/Users/emilynguyen/Desktop/data2")
#csv of unique slugs and basic info about them (date they peaked (if so), how many contributors, size of repo, etc.)
data = read.csv("noUglySlugs.csv")
print(nrow(data))
data$peakFitted = F
data$peakIndex = -1

#traverse through each slug
for(i in 1:nrow(data)) {
  
  #####get historical, long-formatted data on downloads for each slug
  s = shQuote(data$slug[i])
  str = paste("select slug, yearMonth, numDownloads from marxist_NPMImportant120kMonthlySlugA_pydriller_NoOutlier where slug =", s)
  npm <- dbGetQuery(mydb, str)
  if(nrow(npm)>=75) {
    npm = npm[which(npm$slug == npm$slug[1]),]
  }
  #####
  
  #if project has no downloads, it didn't peak. so set peakFitted to false
  if(sum(npm$numDownloads)==0) {
    data$peakFitted[i] = F
    next
  }
  
  #####fit a degree 3, degree 4, and degree 5 polynomial fitted curve to the project's downloads vs time plot
  npm$period = NA
  for(k in 1:nrow(npm)) {
    npm$period[k] = k
  }
  fit3 <- lm(numDownloads~poly(period,3,raw=TRUE), data=npm)
  fit4 <- lm(numDownloads~poly(period,4,raw=TRUE), data=npm)
  fit5 <- lm(numDownloads~poly(period,5,raw=TRUE), data=npm)
  #####
  
  ##### among the 3 fitted curves, find the best fitted curve and go along with that one only
  maxModel = fit3
  max = summary(maxModel)$adj.r.squared
  if(!is.nan(summary(fit4)$adj.r.squared) & summary(fit4)$adj.r.squared > max) {
    maxModel = fit4
    max = summary(fit4)$adj.r.squared
  }
  if(!is.nan(summary(fit5)$adj.r.squared) & summary(fit5)$adj.r.squared > max) {
    maxModel = fit5
    max = summary(fit5)$adj.r.squared
  }
  #####
  
  
  #find index of maximum point of the best fitted curve 
  indMax = which.max(predict(maxModel))
  
  #####find the next minimum after the max of the best fitted curve
  ind = indMax + 1
  while(ind <= (length(npm$period)-1)) {
    #print(paste(i, ":",data$slug[i], (ind-1)))

    if(diff(predict(maxModel))[ind-1] < 0 & diff(predict(maxModel))[ind] > 0 )
      break
    ind = ind + 1
  }
  #####

  #if there is not minimum after the max, just set it to the last index
  if(ind == length(npm$period))
    ind = ind -1

  
  denom = ind - indMax
  numer = predict(maxModel)[ind] - predict(maxModel)[indMax]
  
  if(numer > 0) #we are looking for a negative slope, so numerator must be negative
  {
    print("STOP")
    print(i)
    break
  }
  if(denom == 0) { #check if denominator equals 0
    if(indMax >= (length(npm$period)-3)) {
      #print(i)
      data$peakFitted[i] = F
      next
    }
    if(npm$numDownloads[length(npm$numDownloads)]<0.7*npm$numDownloads[length(npm$numDownloads)-1])
    {
      data$peakFitted[i] = T
      data$peakIndex[i] = indMax
    }
    else
      data$peakFitted[i] = F

     print("denom is 0")
    next
  }

  baseline = -((0.35)*max(npm$numDownloads))/(length(npm$period)/2) #the slope/steepness of the download descent of the fitted curve must be steeper than "baseline"
  baseline2 = -((0.25)*max(npm$numDownloads))/(length(npm$period)/2) #however, if the slope/steepness is less than "baseline," but there's a gradual decrease over a long period of time (say, steeper than a smaller baseline called "baseline2"), we'll count it as peaked

  #if not-as-steep but gradual descent in the fitted surve, peakFitted is set to true
  if(denom >= (0.4*length(npm$period))  & as.numeric(numer)/denom <=baseline2) {
    data$peakFitted[i] = T
      data$peakIndex[i] = indMax
      next
  }

  # if maximum of fitted curve is towards end of data collection (last three months of 2020), but it has a REALLY steep slope, set peakFitted to true
  if(as.numeric(numer)/denom <= baseline) {
    #print(indMax)
    if(indMax>=(length(npm$period) - 3) & as.numeric(numer)/denom < -((0.7)*max(npm$numDownloads))/(length(npm$period)/2)) {
      data$peakFitted[i] = T
      data$peakIndex[i] = indMax
      next
    }
    #if max of the true number of downloads is within the last 3 months, it's too early to assume that it peaked, so set peakFitted to false
    if(indMax>=(length(npm$period) - 3) | which.max(npm$numDownloads) >=(length(npm$numDownloads)-3))
      data$peakFitted[i] = F
    else

    {
      data$peakFitted[i] = T
      data$peakIndex[i] = indMax
    }
  }
  else
    data$peakFitted[i] = F

  if(i%%1000==0)
    print(i)
  
}
