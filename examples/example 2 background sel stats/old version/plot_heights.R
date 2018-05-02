#	plot_heights.R
#
#	Plot tree height versus chromosome position
#
#	Ben Haller, 4/29/2018

setwd("~/DocumentsSynced/Research/Messer lab/SLiM project/Publication TreeSeq/examples/example 3 background sel stats/")
h <- read.csv("ex3_TS_heights.csv")

starts <- h$start
ends <- h$end
heights <- -h$height

x <- t(matrix(c(starts,ends), ncol=2))
y <- rep(heights, each=2)
xr <- range(x)
yr <- pretty(c(0, max(y)), n=1)

# moving average
window <- 10000000
half_window <- window / 2
step <- 10000
center <- 0
ma_x <- NULL
ma_y <- NULL
repeat
{
	mean_height <- 0
	window_left <- center - half_window
	window_right <- center + half_window
	intersecting_rows_left <- (starts < window_right)
	intersecting_rows_right <- (ends > window_left)
	intersecting_rows <- which(intersecting_rows_left & intersecting_rows_right)
	
	height_sum <- 0
	height_weight <- 0
	for (r in intersecting_rows)
	{
		start <- max(starts[r], window_left)
		end <- min(ends[r], window_right)
		len <- end - start + 1
		
		height_sum <- height_sum + heights[r] * len
		height_weight <- height_weight + len
	}
	mean_height <- height_sum / height_weight
	
	# append the data for the window
	ma_x <- c(ma_x, center)
	ma_y <- c(ma_y, mean_height)
	
	# next window
	center <- center + step
	if (center > xr[2])
		break;
}

# plot
quartz(width=5.5, height=2.5, type="pdf", file="dip.pdf")
#quartz(width=5.5, height=2.5)
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="chromosome position", ylab="mean tree height", xaxp=c(xr,1), yaxp=c(yr,1))
lines(x=x, y=y)
abline(v=4e7, col="red", lwd=2)
abline(v=6e7-1, col="red", lwd=2)
lines(x=ma_x, y=ma_y, col="cornflowerblue", lwd=3)
box()
dev.off()



















