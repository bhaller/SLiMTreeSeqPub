#	plot_ancestry.R
#
#	Plot ancestry (mean ancestral subpop) versus chromosome position
#
#	Ben Haller, 4/30/2018

setwd("~/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/example 3 true local ancestry/")
h <- read.csv("ex3_TS_ancestry.csv")

breaks <- h$breaks
ancestry <- h$ancestry

xr <- range(breaks)
yr <- range(ancestry)

# plot
quartz(width=5.5, height=2.75, type="pdf", file="ancestry.pdf")
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="chromosome position", ylab="ancestry proportion", xaxp=c(xr,1), yaxp=c(yr,1), yaxt="n")
axis(side=2, at=c(0,1), labels=c("p1", "p2"))
abline(v=1e8 * 0.2, col="red", lwd=2)
abline(v=1e8 * 0.8, col="red", lwd=2)
lines(x=breaks, y=ancestry, type="s")
box()
dev.off()



















