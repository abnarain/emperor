import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from scipy.stats import norm,rayleigh, expon, entropy
import sys, scipy, getopt, pylab
import numpy as np


# You can compare the log likelihood distance of distributions
# You can compare the mean == That is the expectation of the value (E[nn*])
# You can compare the expectaton using the values in the curve estimated 

def error_calculation(length, param1,param2,param3, param4):
    i=np.arange(length)
    pdf_fitted1 = rayleigh.pdf(i,loc=param1,scale=param2) # fitted distribution
    pdf_fitted2 = rayleigh.pdf(i,loc=param3,scale=param4) # fitted distribution\

    square_err=0
    l1_norm=0
    for i in range(0, length):
        square_err += (pdf_fitted1[i] - pdf_fitted2)**2
        l1_norm += abs(pdf_fitted1[i] - pdf_fitted2)

    mse= square_err*1.0/ length
    mean_l1_norm = 1.0*l1_norm/length  
    print "L1 Norm", l1_norm, " square error =", square_err
    print  "ML1Norm ", mean_l1_norm, "MSE", mse




def expected_value(data):
    return sum(data)*1.0/len(data)

def kl_distance(pk,qk=None):
    return entropy(pk, qk)

def curve_fitting_exp(x,a,b,c):
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
    pylab.figure(0)
    pylab.plot(pdf_fitted)
    pylab.savefig(filename+'_pdf_fitted.pdf')
    pylab.figure(1)
    pylab.hist(data)
    pylab.savefig(filename+'_hist.pdf')

    return param


def calculate_rayleigh(data,filename):
    #x = np.array(x, dtype=float) # gets you rid of slow list comprehension
    values = np.histogram(data) # , density=True)
    cc = values[0]
    param = rayleigh.fit(values[0]) # distribution fitting
    pdf_fitted = rayleigh.pdf(values[1],loc=param[0],scale=param[1]) # fitted distribution
    pylab.figure(0)
    pylab.plot(pdf_fitted)
    pylab.savefig(filename+'_pdf_fitted.pdf')
    pylab.figure(1)
    pylab.hist(data)
    pylab.savefig(filename+'_hist.pdf')

    return param

def main(argv):
    inputfile=''
    ftype=''
    noisefile=''
    noiseflag=0
    try:
        opts, args = getopt.getopt(argv,"h:i:f:n:",["ifile=","ftype=","ntype="])
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
        elif opt in ("-n", "--nfile"):
            noisefile = arg
            noiseflag =1
        elif opt in ("-f", "--ftype"):
            ftype = arg
        else:
            print "check help for usage" 
            sys.exit()

    mag=[]
    mag_noise=[]
    data= scipy.fromfile(open(inputfile), dtype=scipy.complex64)
    for i in range(0,len(data)):
        mag.append(np.absolute(data[i]))

    ps_rayleigh=calculate_rayleigh(mag,'signal_rayleigh')
    print "Signal: rayleigh distribution parameters: expected= ", ps_rayleigh[0], "var is ", ps_rayleigh[1]

    ps_exponential=calculate_exponential(mag,'signal_exponential')
    print "Signal: exponential distribution parameters: expected= ", ps_exponential[0], "var ",ps_exponential[1]

    ps = expected_value(mag)
    print "Signal: expected value acc to time series (E(yy*))  ", ps
    
    print "entropy of signal is ", kl_distance(mag)

    if noiseflag==1:
        noise= scipy.fromfile(open(noisefile), dtype=scipy.complex64)
        for i in range(0,len(noise)):
            mag_noise.append(np.absolute(noise[i]))

        print "For Noise" 
        pn_rayleigh=calculate_rayleigh(mag_noise,'noise_rayleigh')
        print "Noise: rayleigh distribution parameters: expected= ", pn_rayleigh[0], "var is ", pn_rayleigh[1]

        pn_exponential=calculate_exponential(mag_noise,'noise_exponential')
        print "Noise: exponential distribution parameters: expected= ", pn_exponential[0], "var ",pn_exponential[1]

        pn = expected_value(mag_noise)
        print "Noise: Expected value acc to time series (E(nn*)) ", pn
        
        print "the kl distance between th enoise and the signal is=  ", kl_distance(mag,mag_noise)
        print "entropy of Noise is= ", kl_distance(mag_noise)
        min_length = min(len(mag_noise), len(mag))
        print " modelled as exponential distribution " 
        error_calculation(min_length, ps_exponential[0], ps_exponential[1], pn_exponential[0], pn_exponential[1])
        print "\n \n modelled as rayleigh distribution " 
        error_calculation(min_length, ps_rayleigh[0], ps_rayleigh[1], pn_rayleigh[0], pn_rayleigh[1])



if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
