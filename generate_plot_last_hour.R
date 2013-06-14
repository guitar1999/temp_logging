library(RPostgreSQL)
con <- dbConnect(drv="PostgreSQL", host="127.0.0.1", user="jessebishop", dbname="jessebishop")

query <- "select temperature, read_time, device_id from temperature_test where read_time > CURRENT_TIMESTAMP - ((date_part('minute', CURRENT_TIMESTAMP) + 60) * interval '1 minute') - (date_part('second', CURRENT_TIMESTAMP) * interval '1 second');"
res <- dbGetQuery(con, query)

cc <- subset(res, res$device_id == 'current_cost')
ow <- subset(res, res$device_id != 'current_cost')
ow$temperature <- ow$temperature * 9 / 5 + 32

fname <- '/var/www/temperature/last_hours.png'
mintime <- min(res$read_time)
maxtime <- max(res$read_time)
maxtemperature <- ifelse(max(cc$temperature) > max(ow$temperature), max(cc$temperature), max(ow$temperature))
vseq <- seq(0, maxtemperature, ifelse(maxtemperature > 100, 20, 10))
hseq <- seq(mintime, mintime + 7200, 600)

png(filename=fname, width=1024, height=400, units='px', pointsize=12, bg='white')
plot(res$read_time, res$temperature, type='l', col='white', xlim=c(mintime, mintime + 7200), ylim=c(0,maxtemperature), xlab="Time", ylab="Temperature (F)", main=paste("Temperature since ", mintime), xaxt='n', yaxt='n')
axis(side=1, at=hseq, labels=substr(hseq, 12, 16))
axis(side=2, at=vseq, labels=vseq)
abline(v=mintime + 3600, col='black')
abline(h=vseq, col='grey', lty=2)
lines(cc$read_time, cc$temperature, col='red')
lines(ow$read_time, ow$temperature, col='blue')
dev.off()

system(paste("scp", fname, "web309.webfaction.com:/home/jessebishop/webapps/htdocs/home/frompi/electricity/", sep=' '))
