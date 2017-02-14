libraries<-function()
{
	load.lib("wavelets")
	library(wavelets)
}
libraries()
dt<-read.csv2("input.csv")
w <- dwt(dt, filter="haar")
