#	plot_ancestry.R
#
#	Plot ancestry (mean ancestral subpop) versus chromosome position
#
#	Ben Haller, 4/30/2018

setwd("~/DocumentsSynced/Research/Messer lab/SLiM project/Publication TreeSeq/examples/example 3 true local ancestry/")
h <- read.csv("ex3_TS_ancestry.csv")

starts <- h$start
ends <- h$end
subpops <- h$subpop

x <- t(matrix(c(starts,ends), ncol=2))
y <- rep(subpops, each=2)
xr <- range(x)
yr <- range(y)

# plot
quartz(width=5.5, height=2.5, type="pdf", file="ancestry.pdf")
#quartz(width=5.5, height=2.5)
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="chromosome position", ylab="mean ancestry", xaxp=c(xr,1), yaxp=c(yr,1))
abline(v=1e8 * 0.2, col="red", lwd=2)
abline(v=1e8 * 0.8, col="red", lwd=2)
lines(x=x, y=y)
box()
dev.off()



















