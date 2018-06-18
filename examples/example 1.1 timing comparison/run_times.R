#
#	Generate the time comparison figure
#

setwd("~/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/example 1.1 timing comparison")

time_system <- function(command, args, outfile)
{
    if (!file.exists(outfile))
    {
        cat("#", "/usr/bin/time", command, paste(args), "\n")
        system2("/usr/bin/time", args=c(command, args), stdout=outfile, stderr=outfile)
    }
    else
    {
        cat("### skipping run, outfile exists...\n")
    }
	output <- readLines(outfile)
	times <- output[length(output)]
	user <- as.numeric(unlist(regmatches(times, regexec("([0-9.]+) user", times)))[2])
	sys <- as.numeric(unlist(regmatches(times, regexec("([0-9.]+) sys", times)))[2])
	return (user + sys)
}

run_noTS <- function(rep, L)
{
	L_str <- paste0("Lstr=\\\"", L, "\\\"")
	OUTFILE_str <- paste0("OUTFILE=\\\"noTS_L=", L, "_", rep, ".slimbinary\\\"")
	args <- c("-s", rep, "-t", "-m", "-d", L_str, "-d", OUTFILE_str, "./ex1.1_noTS.slim")
	outfile <- paste0("./output/noTS_L=", L, "_", rep, ".slimout")
	time <- time_system("../slim", args=args, outfile)
	return (time)
}

run_TS <- function(rep, L)
{
  L_str <- paste0("Lstr=\\\"", L, "\\\"")
  OUTFILE_str <- paste0("OUTFILE=\\\"TS_L=", L, "_", rep, ".trees\\\"")
  args <- c("-s", rep, "-t", "-m", "-d", L_str, "-d", OUTFILE_str, "./ex1.1_TS.slim")
  outfile <- paste0("./output/TS_L=", L, "_", rep, ".slimout")
  time <- time_system("../slim", args=args, outfile)
  return (time)
}

run_TS_addMuts <- function(rep, L)
{
  INFILE_str <- paste0("TS_L=", L, "_", rep, ".trees")
  args <- c("./msp-add-mutation.py", "--basedir", "./output/", "--tree_file", INFILE_str, "--mut_rate", "1e-7")
  outfile <- paste0("./output/TS_L=", L, "_", rep, "_ADD.txt")
  time <- time_system("/opt/local/bin/python", args=args, outfile)
  return (time)
}

run_msprime <- function(rep, L)
{
    args <- c("./msp-coalescent.py", "--rep", rep, "--length", L)
    outfile <- paste0("./output/msp_L=", L, "_", rep, ".log")
    time <- time_system("/opt/local/bin/python", args=args, outfile)
    return (time)
}

run_msprime_sample <- function(rep, L)
{
    args <- c("./msp-coalescent-sample.py", "--rep", rep, "--length", L)
    outfile <- paste0("./output/msp_L=", L, "_", rep, "_S.log")
    time <- time_system("/opt/local/bin/python", args=args, outfile)
    return (time)
}


# SLiM runs without tree-sequence recording
noTS_1e5 <- sapply(0:9, FUN=function(rep) { run_noTS(rep, "1e5") })
noTS_1e6 <- sapply(0:9, FUN=function(rep) { run_noTS(rep, "1e6") })
noTS_1e7 <- sapply(0:9, FUN=function(rep) { run_noTS(rep, "1e7") })
noTS_1e8 <- sapply(0:9, FUN=function(rep) { run_noTS(rep, "1e8") })
noTS_1e9 <- sapply(0:4, FUN=function(rep) { run_noTS(rep, "1e9") })     # DO MORE RUNS
noTS_1e9 <- rep(NA, 10)    # NOT YET RUN
noTS_1e10 <- rep(NA, 10)    # estimated below, since the memory usage is too high

# SLiM runs with tree-sequence recording
TS_1e5 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e5") })
TS_1e6 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e6") })
TS_1e7 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e7") })
TS_1e8 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e8") })
TS_1e9 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e9") })
TS_1e10 <- sapply(0:9, FUN=function(rep) { run_TS(rep, "1e10") })

# overlay of mutations on top of the previous runs using msprime
TSadd_1e5 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e5") })
TSadd_1e6 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e6") })
TSadd_1e7 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e7") })
TSadd_1e8 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e8") })
TSadd_1e9 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e9") })
TSadd_1e10 <- sapply(0:9, FUN=function(rep) { run_TS_addMuts(rep, "1e10") })

# total time for SLiM + overlay, for the tree-sequence recording runs
TStotal_1e5 <- TS_1e5 + TSadd_1e5
TStotal_1e6 <- TS_1e6 + TSadd_1e6
TStotal_1e7 <- TS_1e7 + TSadd_1e7
TStotal_1e8 <- TS_1e8 + TSadd_1e8
TStotal_1e9 <- TS_1e9 + TSadd_1e9
TStotal_1e10 <- TS_1e10 + TSadd_1e10

# coalescent runs with msprime, sample size n = N
msp_1e5 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e5") })
msp_1e6 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e6") })
msp_1e7 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e7") })
msp_1e8 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e8") })
msp_1e9 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e9") })
msp_1e10 <- sapply(0:9, FUN=function(rep) { run_msprime(rep, "1e10") })

# coalescent runs with msprime, sample size n = N / 100
mspS_1e5 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e5") })
mspS_1e6 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e6") })
mspS_1e7 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e7") })
mspS_1e8 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e8") })
mspS_1e9 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e9") })
mspS_1e10 <- sapply(0:9, FUN=function(rep) { run_msprime_sample(rep, "1e10") })


# compute summary statistics: mean, standard error of the mean
se <- function(x) sqrt(var(x, na.rm=TRUE)/sum(!is.na(x)))

msp_times_mean <- c(mean(msp_1e5), mean(msp_1e6), mean(msp_1e7), mean(msp_1e8), mean(msp_1e9), mean(msp_1e10))
msp_times_se <- c(se(msp_1e5), se(msp_1e6), se(msp_1e7), se(msp_1e8), se(msp_1e9), se(msp_1e10))

mspS_times_mean <- c(mean(mspS_1e5), mean(mspS_1e6), mean(mspS_1e7), mean(mspS_1e8), mean(mspS_1e9), mean(mspS_1e10))
mspS_times_se <- c(se(mspS_1e5), se(mspS_1e6), se(mspS_1e7), se(mspS_1e8), se(mspS_1e9), se(mspS_1e10))

TSslim_times_mean <- c(mean(TS_1e5), mean(TS_1e6), mean(TS_1e7), mean(TS_1e8), mean(TS_1e9), mean(TS_1e10, na.rm=TRUE))
TSslim_times_se <- c(se(TS_1e5), se(TS_1e6), se(TS_1e7), se(TS_1e8), se(TS_1e9), se(TS_1e10))

TStotal_times_mean <- c(mean(TStotal_1e5), mean(TStotal_1e6), mean(TStotal_1e7), mean(TStotal_1e8), mean(TStotal_1e9), mean(TStotal_1e10, na.rm=TRUE))
TStotal_times_se <- c(se(TStotal_1e5), se(TStotal_1e6), se(TStotal_1e7), se(TStotal_1e8), se(TStotal_1e9), se(TStotal_1e10))

noTS_times_mean <- c(mean(noTS_1e5), mean(noTS_1e6), mean(noTS_1e7), mean(noTS_1e8), mean(noTS_1e9, na.rm=TRUE), mean(noTS_1e10, na.rm=TRUE))
noTS_times_se <- c(se(noTS_1e5), se(noTS_1e6), se(noTS_1e7), se(noTS_1e8), se(noTS_1e9), se(noTS_1e10))
noTS_times_sd <- c(sd(noTS_1e5), sd(noTS_1e6), sd(noTS_1e7), sd(noTS_1e8), sd(noTS_1e9), sd(noTS_1e10))


# plot; uncomment the segments() calls to see standard error bars (which are practically invisible)
# the legend() stuff is pretty gross; adjusting the box dimensions in log coordinates...
quartz(width=3.5, height=3.5, type="pdf", file="comparison.pdf")
par(mar=c(3.5, 3.5, 1, 1), family="serif", mgp=c(2.1, 0.6, 0))
plot(x=c(1,6), y=c(0.1,1e6), type="n", xlab="chromosome length", ylab="time (seconds)", xaxp=c(1,6,5), yaxp=c(0.1,1e6,1), xaxt="n", yaxt="n", log="y")
axis(side=1, at=1:6, labels=c(expression(10^5),expression(10^6),expression(10^7),expression(10^8),expression(10^9),expression(10^10)))
axis(side=2, at=10^(-1:6), labels=c(expression(10^-1),expression(10^0),10,expression(10^2),expression(10^3),expression(10^4),expression(10^5),expression(10^6)))

for (base in c(1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6))
    abline(h=base*(1:9), col=c("#AAAAAA", rep("#DDDDDD", times=8)))

lines(x=1:6, y=mspS_times_mean, col="red")
points(x=1:6, y=mspS_times_mean, pch=22, cex=0.75, col="red", bg="white")
#segments(x0=1:6, y0=mspS_times_mean + mspS_times_se, x1=1:6, y1=mspS_times_mean - mspS_times_se, col="blue")

lines(x=1:6, y=msp_times_mean, col="red")
points(x=1:6, y=msp_times_mean, pch=15, cex=0.75, col="red")
#segments(x0=1:6, y0=msp_times_mean + msp_times_se, x1=1:6, y1=msp_times_mean - msp_times_se, col="blue")

lines(x=1:6, y=TSslim_times_mean, col="chartreuse3", lty=3)
points(x=1:6, y=TSslim_times_mean, pch=21, cex=0.75, col="chartreuse3", bg="white")
lines(x=1:6, y=TStotal_times_mean, col="chartreuse3")
points(x=1:6, y=TStotal_times_mean, pch=19, cex=0.75, col="chartreuse3")
#segments(x0=1:6, y0=TStotal_times_mean + TStotal_times_se, x1=1:6, y1=TStotal_times_mean - TStotal_times_se, col="red")

lines(x=1:6, y=noTS_times_mean, col="cornflowerblue")
points(x=1:6, y=noTS_times_mean, pch=23, cex=0.75, col="cornflowerblue", bg="cornflowerblue")
#segments(x0=1:6, y0=noTS_times_mean + noTS_times_se, x1=1:6, y1=noTS_times_mean - noTS_times_se, col="red")

est_noTS6 <- noTS_times_mean[5] * (noTS_times_mean[5] / noTS_times_mean[4])
lines(x=5:6, y=c(noTS_times_mean[5], est_noTS6), col="cornflowerblue", lty=3)
points(x=6, y=est_noTS6, pch=23, cex=0.75, col="cornflowerblue", bg="white")

leg <- legend(x="topleft", legend=c("SLiM (           extrapolated)", "SLiM treeSeq", "SLiM treeSeq (pre-overlay)", expression(paste("msprime coalescent (",italic(n)," = ",italic(N),")")), expression(paste("msprime coalescent (",italic(n)," = ",italic(N),"/100)"))), lty=c(1,1,3,1,2), col=c("cornflowerblue", "chartreuse3", "chartreuse3", "red", "red"), pch=c(23, 19, 21, 15, 22), cex=0.6, pt.cex=0.75, bg="white", inset=c(0.04, 0.015), plot=FALSE)
r <- leg$rect
rect(r$left - 0.06, 10^(r$top + r$h - 2.18), r$left + r$w, 10^(r$top - 2.0), col="white")
leg <- legend(x="topleft", legend=c("SLiM (           extrapolated)", "SLiM treeSeq", "SLiM treeSeq (pre-overlay)", expression(paste("msprime coalescent (",italic(n)," = ",italic(N),")")), expression(paste("msprime coalescent (",italic(n)," = ",italic(N),"/100)"))), lty=c(1,1,3,1,1), col=c("cornflowerblue", "chartreuse3", "chartreuse3", "red", "red"), pt.bg=c("cornflowerblue", "white", "white", "white", "white"), pch=c(23, 19, 21, 15, 22), cex=0.6, pt.cex=0.75, bg="white", inset=c(0.04, 0.015), bty="n")
lines(x=c(2.3, 2.67), y=c(6.5e5, 6.5e5), col="cornflowerblue", lty=3)
points(x=mean(c(2.3, 2.67)), y=6.5e5, pch=23, cex=0.75, col="cornflowerblue", bg="white")

box()
dev.off()


# write out a CSV of the results
df <- data.frame(msp_times_mean, msp_times_se, mspS_times_mean, mspS_times_se, TSslim_times_mean, TSslim_times_se, TStotal_times_mean, TStotal_times_se, noTS_times_mean, noTS_times_se)
write.csv(df, file="comparison.csv", row.names=FALSE)








