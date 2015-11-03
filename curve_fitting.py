import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from scipy.stats import norm,rayleigh, expon
import sys, scipy, getopt, pylab
import numpy as np


def curve_fitting_exp(x,a,b,c)
    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    x = np.linspace(0,4,50)
    y = func(x, 2.5, 1.3, 0.5)
    yn = y + 0.2*np.random.normal(size=len(x))

    popt, pcov = curve_fit(func, x, yn)
    return popt


def calculate_exponential(data,filename):
    #x = np.array(x, dtype=float) # gets you rid of slow list comprehension
    values = np.histogram(data) #, density=True)
    cc = values[0]
    param = expon.fit(values[0]) # distribution fitting - location, scale - mean and MLE estimator 
    pdf_fitted = expon.pdf(values[1],loc=param[0],scale=param[1]) # fitted distribution
    pylab.savefig(filename)
    pylab.savefig(filename+'_pdf_fitted.png')
    pylab.hist(filename+'_hist.png')

    return param


def calculate_rayleigh(data,filename):
    #x = np.array(x, dtype=float) # gets you rid of slow list comprehension
    values = np.histogram(data) # , density=True)
    cc = values[0]
    param = rayleigh.fit(values[0]) # distribution fitting
    pdf_fitted = rayleigh.pdf(values[1],loc=param[0],scale=param[1]) # fitted distribution
    pylab.plot(pdf_fitted)
    pylab.savefig(filename+'_pdf_fitted.png')
    pylab.hist(filename+'_hist.png')

    return param

def main(argv):
    inputfile=''
    ftype=''
    try:
        opts, args = getopt.getopt(argv,"h:i:f:",["ifile=","ftype="])
    except getopt.GetoptError:
        print 'file.py -i <inputfile> -f <caption on graph>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -i <inputfile> -f <caption on graph> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--ftype"):
            ftype = arg
        else:
            print "check help for usage" 
            sys.exit()

    mag=[]
    print "input file is",inputfile
    data= scipy.fromfile(open(inputfile), dtype=scipy.complex64)
    for i in range(0,len(data)):
        mag.append(np.absolute(data[i]))

    ps=calculate_rayleigh(mag,'rayleigh')
    print "rayleigh distribution parameters ", ps

    ps=calculate_exponential(mag'exponential')
    print "exponential distribution parameters: ", ps



if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
