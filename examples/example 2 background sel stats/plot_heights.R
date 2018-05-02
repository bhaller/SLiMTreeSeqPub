#	plot_heights.R
#
#	Plot tree height versus chromosome position
#
#	Ben Haller, 4/29/2018

setwd("~/DocumentsSynced/Research/Messer lab/SLiM project/Publication TreeSeq/examples/example 2 background sel stats/")
h <- read.csv("ex2_TS_heights.csv")

starts <- h$start
ends <- h$end - 1
heights <- h$height
heights <- heights + (-min(heights))

# loop through sites and assimilate their contribution to tree height versus distance from gene
# we skip over positions inside genes, and then count positions out to halfway to the next gene
# genes are at:
#
# initializeGenomicElement(g2, 100000, 100999);
# initializeGenomicElement(g2, 201000, 201999);
# initializeGenomicElement(g2, 302000, 302999);
# ...
L <- 1e8		# total chromosome length
L0 <- 200e3		# between genes
L1 <- 1e3		# gene length
height_for_pos <- rep(0, L)

for (site_index in 1:nrow(h))
{
	site_start <- starts[site_index]
	site_end <- ends[site_index]
	site_height <- heights[site_index]
	height_for_pos[site_start:site_end + 1] <- rep(site_height, site_end - site_start + 1)
}

height_for_left_distance <- rep(0, L0/4)
height_for_right_distance <- rep(0, L0/4)
gene_starts <- seq(from=L0, to=L-(L0+L1), by=(L0+L1))
gene_ends <- gene_starts + L1 - 1
gene_centers <- (gene_starts + gene_ends) / 2

for (distance in 1:(L0/4))
{
	left_positions <- gene_starts - distance
	left_positions <- left_positions[left_positions >= 0]
	mean_height_left <- mean(height_for_pos[left_positions])
	height_for_left_distance[distance] <- mean_height_left
	
	right_positions <- gene_ends + distance
	right_positions <- right_positions[right_positions <= L-1]
	mean_height_right <- mean(height_for_pos[right_positions])
	height_for_right_distance[distance] <- mean_height_right
}

height_for_distance <- c(rev(height_for_left_distance), height_for_right_distance)

# plot
x <- c((-L0/4):-1, 1:(L0/4))
y <- height_for_distance
xr <- range(x)
yr <- c(25000, 35000)

quartz(width=5.5, height=2.5, type="pdf", file="dip.pdf")
#quartz(width=5.5, height=2.5)
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=xr, y=yr, type="n", xlab="distance from gene", ylab="mean tree height", xaxp=c(xr,2), yaxp=c(yr,1))
lines(x=x, y=y)
box()
dev.off()



# synthesize data for testing; seems to work
starts <- NULL
ends <- NULL
heights <- NULL
starts_temp <- NULL
ends_temp <- NULL
heights_temp <- NULL
finished_pos <- -1

repeat
{
	next_start <- finished_pos + 1
	next_end <- next_start + round(runif(1, min=10, max=1000))
	if (next_end > L - 1)
		next_end <- L - 1
	center <- (next_start + next_end) / 2
	d <- min(abs(gene_centers - center))
	height <- runif(1, min=0.79+(d/(L0/2))*0.1, max=0.99+(d/(L0/2))*0.1)
	
	starts_temp <- c(starts_temp, next_start)
	ends_temp <- c(ends_temp, next_end)
	heights_temp <- c(heights_temp, height)
	
	if (length(starts_temp) == 1000)
	{
		starts <- c(starts, starts_temp)
		ends <- c(ends, ends_temp)
		heights <- c(heights, heights_temp)
		starts_temp <- NULL
		ends_temp <- NULL
		heights_temp <- NULL
	}
	
	if (finished_pos %/% 1000000 != next_end %/% 1000000)
		cat(paste0("start ", next_start, ", end ", next_end, ", height ", height, "\n"))
	
	finished_pos <- next_end
	if (finished_pos >= L - 1)
		break;
}

starts <- c(starts, starts_temp)
ends <- c(ends, ends_temp)
heights <- c(heights, heights_temp)












