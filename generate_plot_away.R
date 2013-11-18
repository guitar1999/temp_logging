library(RPostgreSQL)
con <- dbConnect(drv="PostgreSQL", host="127.0.0.1", user="jessebishop", dbname="jessebishop")

query <- "select temperature, read_time, device_id from temperature_test where read_time > '2013-10-23';"
res <- dbGetQuery(con, query)

res$temperature <- res$temperature * 9 / 5 + 32

fname <- '/var/www/temperature/away.png'
mintime <- min(res$read_time)
maxtime <- max(res$read_time)
maxtemperature <- max(res$temperature)
vseq <- seq(0, maxtemperature, ifelse(maxtemperature > 100, 20, 2))
hseq <- seq(mintime, mintime + 7200, 600)

png(filename=fname, width=1024, height=400, units='px', pointsize=12, bg='white')
plot(res$read_time, res$temperature, type='l', col='white', xlim=c(mintime, maxtime), ylim=c(min(res$temperature),maxtemperature), xlab="Time", ylab="Temperature (F)", main=paste("Temperature since ", mintime))#, xaxt='n', yaxt='n')
#axis(side=1, at=hseq, labels=substr(hseq, 12, 16))
#axis(side=2, at=vseq, labels=vseq)
#abline(v=mintime + 3600, col='black')
abline(h=vseq, col='grey', lty=2)
lines(res$read_time, res$temperature, col='red')
dev.off()

system(paste("scp", fname, "web309.webfaction.com:/home/jessebishop/webapps/htdocs/home/frompi/electricity/", sep=' '))
