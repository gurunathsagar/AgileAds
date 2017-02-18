### R code for CSIRO 1-day workshop `Wavelet Methods for Time Series Analysis'
###
### Part I: Introduction to Wavelets and Wavelet Transforms

### Four R packages were mentioned at the beginning of the workshop as particularly
### useful for learning about - and conducting - wavelet analyis of time series:
### wmtsa, wavelets, waveslim and wavethresh.  The code in this file makes use of
### just wmtsa and some auxillary R code developed for the workshop.  The package
### wmtsa is on cran and can be installed via the following R command:
###
###    install.packages("wmtsa")
###
### The packages wavelets and waveslim can be installed in a similar manner using
### the following R commands:
###
###    install.packages("wavelets")
###    install.packages("waveslim")
###
### There is a version of Guy Nason's WaveThresh on cran, but, as of 25 Feb 2010,
### it was obsolete.  To get the latest version (which will eventually be on cran),
### go to
###    http://www.stats.bris.ac.uk/~wavethresh/
### The Mac version of the library can be installed using
###    R CMD INSTALL wavethresh4
### There are also some auxillary functions that are not part of WaveThresh.  These can
### be obtained from
###    http://www.stats.bris.ac.uk/~wavethresh/Book/
### in the form of a file called WaveletFigures.RData, which needs to be loaded:
###    load("/Users/ied/R/GuyNason/WaveletFigures.RData")

library(wmtsa)

### library(wavelets)
### library(waveslim)
### library(wavethresh)

### load auxillary functions and data from downloaded file or from Internet

### print(load(file="/Textures/wavelet-book/courses-wavelets/Sydney-2010/workshop.Rdata"))

con <- url("http://faculty.washington.edu/dbp/R-CODE/workshop.Rdata")
print(load(con))
close(con)

### look at oxygen isotope time series

lplot(oxygen)
abline(h=mean(oxygen),lty="dotted",col="red")

### default analysis: full DWT using LA(8) wavelet (coded as "s8")

ox.dwt.01 <- wavDWT(oxygen)  #compute DWT of oxygen isotope series
ox.dwt.01  # tells which wavelet was used, length of series, number of levels etc
ox.dwt.01[["d6"]]     # accesses level 6 wavelet coefficients
ox.dwt.01[[6]]        # also accesses level 6 wavelet coefficients
ox.dwt.01[["s8"]]     # accesses level 8 scaling coefficients (there is just one)
ox.dwt.01[[9]]        # also accesses single scaling coefficient
ox.dwt.01[["extra"]]  # accesses extra coefficients (these are scaling coefficients
                      # that are preserved when there are an odd number of scaling
                      # coefficients at a particular scale
sapply(ox.dwt.01$data,length)  # computes the number of coefficients in each DWT component
                               # (note that there are 11 and 5 wavelet coefficients at
                               # levels 5 and 6, which is where one scaling coefficient
                               # each was peeled off and saved as an extra coefficinte)
sum(sapply(ox.dwt.01$data,length))  # confirm that there are 352 DWT coefficients in all
                                    # (the same as the number of values in the oxygen series)
sapply(ox.dwt.01$data,ss)       # compute sum of squares for each group of coefficients
sum(sapply(ox.dwt.01$data,ss))  # sum of squares of all DWT coefficients
ss(oxygen)                      # sum of squares of original time series
sum(sapply(ox.dwt.01$data,ss)) - ss(oxygen)  # should be close to zero

summary(ox.dwt.01)  # give a numerical summary of DWT 
length(ox.dwt.01$data)  # number of DWT components (8 sets of wavelets + 1 set of scaling
                        # coefficients + 1 set of extra coefficients (there are two of these,
                        # and these are single scaling coefficients from levels 5 and 6)
length(ox.dwt.01$data[[1]])  # number of unit level wavelet coefficients (i.e., level j=1)

plot(ox.dwt.01)  # plot of DWT - this isn't look very informative because single scaling
                 # coefficient is so much larger than all the wavelet coefficients

c.oxygen <- oxygen - mean(oxygen)  # create centered version of oxygen isotope time series

ox.dwt.02 <- wavDWT(c.oxygen)  # DWT of centered oxygen isotope time series
sapply(ox.dwt.01$data,ss)      # compare sum of squares of uncentered versus
sapply(ox.dwt.02$data,ss)      # centered DWT components - note that terms dictated by
                               # scaling coefficients (s8 and extra) are now much smaller
sapply(ox.dwt.01$data,ss) - sapply(ox.dwt.02$data,ss)  # direct comparison
sum(sapply(ox.dwt.02$data,ss)) # compare sum of squares of DWT coefficients with
ss(c.oxygen)                   # sum of squares of centered time series
sum(sapply(ox.dwt.02$data,ss)) - ss(c.oxygen)  # direct comparison
plot(ox.dwt.02)  # plot of DWT now shows structure of wavelet coefficients (d1 to d8)

### decomposing X into Haar-based W_1 and V_1 (see overhead I-55)

ox.dwt.03 <- wavDWT(c.oxygen,n.levels=1,wave="haar",keep.series=TRUE)
plot(ox.dwt.03)
plot(ox.dwt.03,typ="l")
plot(ox.dwt.03[[1]],typ="l")
plot(ox.dwt.03[[2]],typ="l")

### synthesizing X from D_1 and S_1 (see overhead I-58)

plot(wavMRD(ox.dwt.03))

### first level variance decomposition (see overhead I-60)

round(sapply(ox.dwt.03$data,ss)/length(c.oxygen),3)       # 0.295 2.909
round(sum(sapply(ox.dwt.03$data,ss))/length(c.oxygen),3)  # 3.204
round(my.var(c.oxygen),3)                                 # 3.204

### decomposing X into Haar-based W_1, W_2, W_3, W_4  and V_4 (see overhead I-75)

ox.dwt.04 <- wavDWT(c.oxygen,n.levels=4,wave="haar",keep.series=TRUE)
plot(ox.dwt.04)
plot(ox.dwt.04,typ="l")

### example of MRA from J_0=4 partial Haar DWT (see overhead I-76)

plot(wavMRD(ox.dwt.04))

### example of variance decomposition (see overhead I-77)

round(sapply(ox.dwt.04$data,ss)/length(c.oxygen),3)       # 0.295 0.464 0.652 0.846 0.947
round(sum(sapply(ox.dwt.04$data,ss))/length(c.oxygen),3)  # 3.204
round(my.var(c.oxygen),3)                                 # 3.204

### let's look at some wavelet/scaling filters ...

plot(wavDaubechies("haar",norm=FALSE))
plot(wavDaubechies("d4",norm=FALSE))
plot(wavDaubechies("s8",norm=FALSE))   ### LA(8) filter

### overhead I-78

plot(wavEquivFilter("haar",1),typ="h")
plot(wavEquivFilter("haar",2),typ="h")
plot(wavEquivFilter("haar",3),typ="h")
plot(wavEquivFilter("haar",4),typ="h")
plot(wavEquivFilter("haar",1,scaling=TRUE),typ="h")
plot(wavEquivFilter("haar",2,scaling=TRUE),typ="h")
plot(wavEquivFilter("haar",3,scaling=TRUE),typ="h")
plot(wavEquivFilter("haar",4,scaling=TRUE),typ="h")

### overhead I-79

plot(wavEquivFilter("d4",1),typ="h")
plot(wavEquivFilter("d4",2),typ="h")
plot(wavEquivFilter("d4",3),typ="h")
plot(wavEquivFilter("d4",4),typ="h")
plot(wavEquivFilter("d4",1,scaling=TRUE),typ="h")
plot(wavEquivFilter("d4",2,scaling=TRUE),typ="h")
plot(wavEquivFilter("d4",3,scaling=TRUE),typ="h")
plot(wavEquivFilter("d4",4,scaling=TRUE),typ="h")

### overhead I-80

plot(wavEquivFilter("s8",1),typ="h")
plot(wavEquivFilter("s8",2),typ="h")
plot(wavEquivFilter("s8",3),typ="h")
plot(wavEquivFilter("s8",4),typ="h")
plot(wavEquivFilter("s8",1,scaling=TRUE),typ="h")
plot(wavEquivFilter("s8",2,scaling=TRUE),typ="h")
plot(wavEquivFilter("s8",3,scaling=TRUE),typ="h")
plot(wavEquivFilter("s8",4,scaling=TRUE),typ="h")

### overhead I-81

plot(wavGain("s8",n.levels=4,norm=FALSE))

### overhead I-87

ox.modwt.01 <- wavMODWT(c.oxygen,n.levels=4,keep.series=TRUE)
plot(ox.modwt.01,typ="l")
plot(wavShift(ox.modwt.01),typ="l")

### demonstrate extracting DWT from MODWT (cf. overhead I-88)

plot(4*as.vector(ox.modwt.01$data[[4]])[seq(16,length(c.oxygen),16)])
points(as.vector(ox.dwt.02$data[[4]]),pch="+",col="red")

### example of MRA from J_0=4 Haar MODWT (see overhead I-89)

plot(wavMRD(ox.modwt.01))

### example of variance decomposition (see overhead I-90)

round(sapply(ox.modwt.01$data,ss)/length(c.oxygen),3)       # 0.145 0.500 0.751 0.839 0.969 
round(sum(sapply(ox.modwt.01$data,ss))/length(c.oxygen),3)  # 3.204
round(my.var(c.oxygen),3)                                   # 3.204

