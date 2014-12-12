data = read.csv("results.csv")
data = subset(data, data$Answer.S1 == "false" &
                data$Answer.S2 == "ct" &
                data$Answer.S4 == "true")
attach(data)
table(Answer.S1)
table(Answer.S2)
table(Answer.S3)
table(Answer.S4)

