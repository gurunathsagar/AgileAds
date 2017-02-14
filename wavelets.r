load.lib<-function(libT,l=NULL)
{
	lib.loc <- l
	print(lib.loc)
	
	if (length(which(installed.packages(lib.loc=lib.loc)[,1]==libT))==0)
	{
		install.packages(libT, lib=lib.loc,repos='http://cran.us.r-project.org')
	}
}

libraries<-function()
{
	load.lib("wavelets")
	library(wavelets)
}
libraries()
dt<-read.csv2("input.csv")
w <- dwt(dt, filter="haar")
