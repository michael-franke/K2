# data = read.csv('data.csv')

require('plyr')

response = 0

for (i in 1:nrow(data)){
  respVec = data[i,c("X1", "X2", "X3", "X4")]
  respVec[is.na(respVec)] = 0
  response[i] = sum(respVec)
}

data$response = response

data$correctBin = ifelse(data$correct == "True", 1, 0)
meanSuccess = ddply(subset(data, data$type == "control"), .(id), summarise, mymean = mean(correctBin))
table(meanSuccess$mymean)

for (i in 1:nrow(data)){
  data$meanSuccess[i] = meanSuccess[data[i,]$id,"mymean"]
}

dataClean = subset(data, data$meanSuccess >= 0.5)
critical = subset(dataClean, dataClean$type == "critical")
table(critical$response)

meanSuccessSentence = ddply(subset(data, data$type == "control"), .(sentence), summarise, mymean = mean(correctBin))
data[grepl("3", data$sentence),"type"] = "control 1"


# to do:
# 1.) get success rates for each participant
# 2.) throw out guys who did too badly (more than 2 mistakes)
# 3.) get control number
# 4.) check if guys were able to give judgements early

