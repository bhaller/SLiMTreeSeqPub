#	plot_heights.R
#
#	Plot tree height versus distance from gene, from a saved CSV file
#
#	Ben Haller, 8/26/2018

setwd("~/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/example 4 neutral burn-in/")
h_decap <- read.csv("ex4_TS_decap_heights.csv")
h_recap <- read.csv("ex4_TS_recap_heights.csv")

x <- h_recap$start
y <- log10(h_recap$height)

xr <- range(x)
yr <- c(floor(min(y)), ceiling(max(y)))

quartz(width=5.5, height=2.5, type="pdf", file="recapitation.pdf")
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="chromosome position", ylab="log(mean tree height)", xaxp=c(xr,1), yaxp=c(yr,1))
lines(x=h_decap$start, y=log10(h_decap$height), type="s", col="red", lwd=1.5)
lines(x=x, y=y, type="s", lwd=0.5)
box()
dev.off()
