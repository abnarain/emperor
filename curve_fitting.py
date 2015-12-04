import sys, scipy, getopt, matplotlib, pickle
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
import numpy as np
from scipy.stats import norm,rayleigh, expon, entropy
from scipy.optimize import curve_fit
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from sklearn.metrics import mean_squared_error
from math import sqrt,log

# Can be used to adjust the border and spacing of the figure    
fig_width = 10
fig_length = 10.25
fig_left = 0.12
fig_right = 0.94
fig_bottom = 0.25
fig_top = 0.94
fig_hspace = 0.5
column,row=1,1

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

# You can compare the log likelihood distance of distributions
# You can compare the mean == That is the expectation of the value (E[nn*])
# You can compare the expectaton using the values in the curve estimated 

def error_calculation(bins, param_s1,param_s2,param_n1, param_n2, flag):
    if flag==1:
        pdf_fitted1 = rayleigh.pdf(bins,loc=param_s1,scale=param_s2) # fitted distribution - rayleigh
        pdf_fitted2 = rayleigh.pdf(bins,loc=param_n1,scale=param_n2) # fitted distribution - rayleigh
    elif flag==0:
        pdf_fitted1 = expon.pdf(bins,loc=param_s1,scale=param_s2) # fitted distribution - exponential
        pdf_fitted2 = expon.pdf(bins,loc=param_n1,scale=param_n2) # fitted distribution - exponential
    l1_norm=0
    mean_square_err =mean_squared_error(pdf_fitted1, pdf_fitted2)
    l1_norm = sum(abs(pdf_fitted1[i] - pdf_fitted2))

    root_mean_square_err = sqrt(mean_square_err)
    mean_l1_norm = 1.0*l1_norm/length
    print "Root Mean Square Error= ", root_mean_square_err
    print "Mean L1 norm= ", mean_l1_norm 

def kl_distance(pk,qk=None):
    '''
    One has to remember that KL divergence is done for two probability distributions 
    and not a data series, so first get the normalized histogram to feed into this.
    One can also first estimate the distribution and then feed it to get the distribution.
    '''
    if qk != None:
        min_len = min(len(pk),len(qk))
        return entropy(pk[:min_len], qk[:min_len],base=2)
    else:    
        return entropy(pk, qk,base=2)


def curve_fitting_exp(data):
    n, bins= np.histogram(data,200,density=1)
    xdata =bins[0:len(n)]
    ydata=n
    def fitfuncRayleigh (x, a,b,c,d):
        return x*a/(b**2)*exp(-0.5*((x-c)/b)**2)+d

    def fitfuncGaussian(x,a,b,c,d):
        return a*exp(-0.5*((x-b)/a)**2)+d

    def fitfuncExp (x,a,b,c,d):
        return  a*exp((x-b)*a)+c 

    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    popt, pcov = curve_fit(func, xdata, ydata)
    return popt
def approximating_dists(data,bins):
    try :
        rayleigh_param = rayleigh.fit(data)
    except:
        print "screwed raleigh fit "
    print "params for rayleigh " ,rayleigh_param

    try:
        pdf_rayleigh_fitted = rayleigh.pdf(bins, *rayleigh_param[:-2],loc=rayleigh_param[0],scale=rayleigh_param[1]) # fitted distribution
    except :
        print " returning as nothing to plot "

    try :
        exp_param = expon.fit(data)
    except:
        print "screwed expon fit "
    print "params for exponential ", exp_param

    try:
        pdf_exp_fitted = expon.pdf(bins, *exp_param[:-2],loc=exp_param[0],scale=exp_param[1]) # fitted distribution
    except :
        print " returning as nothing to plot "
    return [exp_param, pdf_exp_fitted, rayleigh_param, pdf_rayleigh_fitted]


def main(argv):
    inputfile,onesfile,noisefile,niqfile,oiqfile='','','','',''
    noiseflag, onesflag, noiseflag1, onesflag1=0,0,0,0
    print " main "
    try:
        opts, args = getopt.getopt(argv,"h:i:o:n:y:x::",["ifile=","ofile=","ntype=","oiqfile","niqfile="])
    except getopt.GetoptError:
        print 'file.py -i <inputfile> -n <noise stats> -o <ones stats> -x <noise iq file> -y <ones iq file>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -i <inputfile> -n <noise stats> -o<ones stats> -x <noise iq file> -y <ones iq file>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--nfile"):
            noisefile = arg
            noiseflag1=1
        elif opt in ("-o", "--ofile"):
            onesfile = arg
            onesflag1=1
        elif opt in ("-y", "--oiqfile"):
            oiq_file = arg
            onesflag=1
        elif opt in ("-x", "--niqfile"):
            niq_file = arg
            noiseflag=1
        else:
            print "check help for usage" 
            sys.exit()

    assert(noiseflag==1 and noiseflag1==1), " Set all the files correctly for noise "
    #assert(onesflag==1 and onesflag1 ==1), " Set all the files correctly for ones "

    z_data= scipy.fromfile(open(inputfile), dtype=scipy.complex64)
    l=inputfile.split('_')
    print "\nthe elements are: ", l[-3][-2:], l[-1]
    fname= '_'.join([l[-3][-2:] , l[-2], l[-1][:-4]])

    print "filename is " , fname
    
    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom =
    fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig1.add_subplot(1,1,1)

    data=map(np.absolute,z_data)
    data_hist, data_bins= np.histogram(data,200,density=1)
    [data_exp_param, data_pdf_exp_fitted, data_rayleigh_param, data_pdf_rayleigh_fitted] = approximating_dists(data,data_bins)
    print "Entropy of transmission ", kl_divergence(data_pdf_rayleigh_fitted)
    print "data exp param ",data_exp_param, "data rayleigh param ", data_rayleigh_param
    _subplot.hist(data,200,facecolor='red', alpha=0.6, normed=1, label= 'data')
    _subplot.plot(data_bins,data_pdf_rayleigh_fitted,'r-',label='data estimate rayleigh')
    _subplot.plot(data_bins,data_pdf_exp_fitted,'r^', label='data estimate exp')
    
    if noiseflag==1 and noiseflag==1:
        z_noise= scipy.fromfile(open(niq_file), dtype=scipy.complex64)
        noise =map(np.absolute,z_noise)
        noise_hist, noise_bins= np.histogram(noise,200,density=1)
        _subplot.hist(noise,200,normed=1,alpha=0.5, facecolor='blue', label='noise')

        [noise_exp_param, noise_pdf_exp_fitted, noise_rayleigh_param, noise_pdf_rayleigh_fitted]= pickle.load(open(noisefile, "rb" ))
        _subplot.plot(noise_bins,noise_pdf_rayleigh_fitted,'b-', label='noise estimate rayleigh')
        _subplot.plot(noise_bins,noise_pdf_exp_fitted,'b^', label='noise estimate exp')
        print "Entropy of noise " , kl_divergence(noise_pdf_rayleigh_fitted)
        print "KL Divergence of data wrt noise(rayleigh) ", kl_divergence(data_pdf_rayleigh_fitted, noise_pdf_rayleigh_fitted)

        print "\n modelled as exponential distribution "
        error_calculation(noise_bins, data_exp_param[0], data_exp_param[1], noise_exp_param[0], noise_exp_param[1],0)
        print "\n modelled as rayleigh distribution "
        error_calculation(noise_bins, data_rayleigh_param[0], data_rayleigh_param[1], noise_rayleigh_param[0], noise_rayleigh_param[1],1)

    if onesflag==1 and onesflag1==1:
         z_ones= scipy.fromfile(open(oiq_file), dtype=scipy.complex64)
         ones =map(np.absolute,z_ones)
         ones_hist, ones_bins= np.histogram(ones,200,density=1)
         _subplot.hist(ones,200,normed=1,alpha=0.8, facecolor='green', label='ones')

         [ones_exp_param, ones_pdf_exp_fitted, ones_rayleigh_param, ones_pdf_rayleigh_fitted] = pickle.load(open(onesfile, "rb" ))
         _subplot.plot(ones_bins,ones_pdf_rayleigh_fitted,'g-', label='ones estimate rayleigh')
         _subplot.plot(ones_bins,ones_pdf_exp_fitted,'g^', label='ones estimate exp')


    _subplot.legend()
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(fname+'.pdf', dpi = 110)


if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
