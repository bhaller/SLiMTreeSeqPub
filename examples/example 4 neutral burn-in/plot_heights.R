#	plot_heights.R
#
#	Plot tree height versus distance from gene, from a saved CSV file
#
#	Ben Haller, 8/26/2018

setwd("~/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/example 4 neutral burn-in/")
h_decap <- read.csv("ex4_TS_decap_heights.csv")
h_recap <- read.csv("ex4_TS_recap_heights.csv")

x <- h_recap$start
y <- h_recap$height ^ 0.33

xr <- range(x)
yr <- c(1, 100)

quartz(width=5.5, height=2.75, type="pdf", file="recapitation.pdf")
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="chromosome position", ylab="mean tree height (generations)", xaxp=c(xr,1), yaxp=c(yr,1), yaxt="n")
axis(side=2, at=c(1, 1e4^0.33, 1e5^0.33, 1e6^0.33), labels=c("1", "1e4", "1e5", "1e6"))
lines(x=h_decap$start, y=h_decap$height^0.33, type="s", col="red", lwd=2.0)
lines(x=x, y=y, type="s", lwd=1.0)
box()
dev.off()

