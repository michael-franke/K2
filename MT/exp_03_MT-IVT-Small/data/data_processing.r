require('plyr')

data = read.csv('data.csv')

response = 0

for (i in 1:nrow(data)){
  respVec = data[i,c("X1", "X2", "X3", "X4")]
  respVec[is.na(respVec)] = 0
  response[i] = sum(respVec)
}

data$response = response

# total counts for all participants:
### errors: 7, semantic: 66, pragmatic 27
table(subset(data, data$type == "critical")$response)

data$correctBin = ifelse(data$correct == "True", 1, 0)
meanSuccess = ddply(subset(data, data$type == "control"), .(id), summarise, mymean = mean(correctBin))
table(meanSuccess$mymean)

for (i in 1:nrow(data)){
  data$meanSuccess[i] = meanSuccess[data[i,]$id,"mymean"]
}

dataClean = droplevels(subset(data, data$meanSuccess >= 0.5))

# number of participants total: 50
length(levels(data$id))
# number of participants who had at least two of the four controls correct: 39
length(levels(dataClean$id))
# number of participants discarded for bad performance: 11


# counts for answer types out of 2*39 = 68 in total:
### semantic: 55, pragmatic: 21, errors: 2
critical = droplevels(subset(dataClean, dataClean$type == "critical"))
table(critical$response)

# check if participants were either semantic OR pragmatic responders:
### switchers: 2, mistakers: 2, semantic responders: 26, pragmatic responders: 9
table(critical$id,critical$response)
