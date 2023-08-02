library(caret)
library(tidyverse)
library(ISLR)
library(ggplot2)
library(car)
library(pscl)

setwd("/Users/emilynguyen/Desktop/data2")
data = read.csv("noUglySlugs.csv")

#if this model throws errors, try converting some variables to a factor, integer, or numeric (i.e. as.factor(peaked), as.integer(monSinceLastOpIssue), or as.numeric(size), etc.)
object <- glm(peakFitted ~ archivedOrDepr + log(monSinceLastOpIssue+1) + log(monSinceLastCommOrClosedIssue+1) + log(commitsUpToPeak+1) + log(issuesOpenedUpToPeak+1)  + log(versionsUpTo+1) + log(downloadsAtPeak+1) + log(age+1) + log(size+1)+ log(contributorsToLastComm+1), data = data, family = "binomial", na.action = na.exclude)


summary(object)
plot(object)
vif(object)
coef(object)
exp(coefficients(object))
pR2(object)