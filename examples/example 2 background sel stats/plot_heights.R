#	plot_heights.R
#
#	Plot tree height versus distance from gene, from a saved CSV file
#
#	Ben Haller, 4/29/2018

setwd("~/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/example 2 background sel stats/")
h <- read.csv("ex2_TS_heights.csv")

x <- h$distance
y <- h$height

xr <- range(x)
yr <- c(25000, 35000)

quartz(width=5.5, height=2.5, type="pdf", file="dip.pdf")
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="distance from gene", ylab="mean tree height", xaxp=c(xr,2), yaxp=c(yr,1))
abline(v=0, col="red", lwd=2)
lines(x=x, y=y)
box()
dev.off()
