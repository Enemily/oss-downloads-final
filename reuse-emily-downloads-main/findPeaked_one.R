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
  
  #if maximum occurs during the last month (2020-12), set peakFitted to false
  if(indMax == length(npm$period)) {
    data$peakFitted[i]= F
    next
  }
  #else set peakFitted to true (the project "peaked")
  else {
    data$peakFitted[i] = T
    data$peakIndex[i] = indMax
  }
  
  
  if(i%%1000==0)
    print(i)
  
}
