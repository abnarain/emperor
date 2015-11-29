import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from scipy.stats import norm,rayleigh, expon, entropy
import sys, scipy, getopt
import matplotlib.font_manager
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from math import sqrt,log

fig_width = 10
fig_length = 10.25
# Can be used to adjust the border and spacing of the figure    
fig_left = 0.12
fig_right = 0.94
fig_bottom = 0.25
fig_top = 0.94
fig_hspace = 0.5
column,row=1,1

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

fitfunc  = lambda p, x: p[0]*exp(-0.5*((x-p[1])/p[2])**2)+p[3]
errfunc  = lambda p, x, y: (y - fitfunc(p, x))

# You can compare the log likelihood distance of distributions
# You can compare the mean == That is the expectation of the value (E[nn*])
# You can compare the expectaton using the values in the curve estimated 

def error_calculation(length, param_s1,param_s2,param_n1, param_n2, flag):
    i=np.arange(length)
    if flag==1:
        pdf_fitted1 = rayleigh.pdf(i,loc=param_s1,scale=param_s2) # fitted distribution - rayleigh
        pdf_fitted2 = rayleigh.pdf(i,loc=param_n1,scale=param_n2) # fitted distribution - rayleigh
    elif flag==0:
        pdf_fitted1 = expon.pdf(i,loc=param_s1,scale=param_s2) # fitted distribution - exponential
        pdf_fitted2 = expon.pdf(i,loc=param_n1,scale=param_n2) # fitted distribution - exponential
    l1_norm=0
    mean_square_err =mean_squared_error(pdf_fitted1, pdf_fitted2)
    l1_norm = sum(abs(pdf_fitted1[i] - pdf_fitted2))

    root_mean_square_err = sqrt(mean_square_err)
    mean_l1_norm = 1.0*l1_norm/length
    #print "Mean Square error= ", mean_square_err 
    #print  "L1 norm= ",  l1_norm 
    print "Root Mean Square Error= ", root_mean_square_err
    print "Mean L1 norm= ", mean_l1_norm 

def kl_distance(pk,qk=None):
    if qk != None:
        min_len = min(len(pk),len(qk))
        return entropy(pk[:min_len], qk[:min_len])
    else:    
        return entropy(pk, qk)


def curve_fitting_exp(x,a,b,c):
    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    x = np.linspace(0,4,50)
    y = func(x, 2.5, 1.3, 0.5)
    yn = y + 0.2*np.random.normal(size=len(x))

    popt, pcov = curve_fit(func, x, yn)
    return popt

def calculate_exponential(data,outfile_name):
    n,bins =  np.histogram(data, density=True)  # #_subplot.hist(data,bins=1200,density=1) 
    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot1 = fig1.add_subplot(1,1,1)
    try:
        param = expon.fit(data) # distribution fitting - location, scale - mean and MLE estimator 
    except:
        print " exponential fit not working "
    try:
        pdf_fitted = expon.pdf(bins,loc=param[0],scale=param[1]) # fitted distribution
    except:
        print " the exp pdf dint work, returning ..."
        return [0,0]
    _subplot1.plot(pdf_fitted)
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(outfile_name+'_pdf_fitted.pdf', dpi = 110)

    return param

def calculate_rayleigh(data,outfile_name):
    n, bins=  np.histogram(data,density=1) 
    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot1 = fig1.add_subplot(1,1,1)
    try : 
        param = rayleigh.fit(data) # distribution fitting - location, scale - mean and MLE estimator 
    except:
        print "screwed raleigh fit "
    try:
        pdf_fitted = rayleigh.pdf(bins,loc=param[0],scale=param[1]) # fitted distribution
    except :
        print " returning as nothing to plot "
        return [0,0]

    _subplot1.plot(pdf_fitted)
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(outfile_name+'_pdf_fitted.pdf', dpi = 110)
    return param


def main(argv):
    inputfile=''
    ftype=''
    noisefile=''
    noiseflag=0
    try:
        opts, args = getopt.getopt(argv,"h:i:f:n:",["ifile=","ftype=","ntype="])
    except getopt.GetoptError:
        print 'file.py -i <inputfile> -f <caption on graph> -n <noisefile>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -i <inputfile> -f <caption on graph>  -n <noisefile>'
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

    mag, mag_noise, avg_mag, avg_noise=[],[], [], []
    data= scipy.fromfile(open(inputfile), dtype=scipy.complex64)
    l=inputfile.split('_')
    print "\nthe elements are: ", l[-3][-2:], l[-1]
    fname= '_'.join([l[-2],  l[-3][-2:] ,l[-1][:-4]])

    print "filename is " , fname
    for i in range(0,len(data)):
        mag.append(np.absolute(data[i]))
    avg_mag=movingaverage(mag ,10)
    ps_rayleigh= calculate_rayleigh(mag,'signal_rayleigh'+fname)
    avg_ps_rayleigh= calculate_rayleigh(avg_mag,'avg_signal_rayleigh'+fname)

    mag= mag
    avg_mag=avg_mag
    print "Signal: rayleigh distribution parameters: expected= ", ps_rayleigh[0], "scale is ", ps_rayleigh[1]
    print "Avg Signal: rayleigh distribution parameters: expected= ", ps_rayleigh[0], "scale is ", ps_rayleigh[1]

    ps_exponential= calculate_exponential(mag,'signal_exponential'+fname)
    avg_ps_exponential= calculate_exponential(avg_mag,'avg_signal_exponential'+fname)
    print "Signal: exponential distribution parameters: expected= ", ps_exponential[0], "scale is ",ps_exponential[1]
    print "Avg Signal: exponential distribution parameters: expected= ",avg_ps_exponential[0], "scale is ",avg_ps_exponential[1]

    try:
        print "entropy of signal is= ", kl_distance(mag)
    except:
        print "dint get signal entropy "

    if noiseflag==1:
        noise= scipy.fromfile(open(noisefile), dtype=scipy.complex64)
        for i in range(0,len(noise)):
            mag_noise.append(np.absolute(noise[i]))
        avg_noise=movingaverage(mag_noise ,10)
        mag_noise =mag_noise
        avg_noise =avg_noise
        print "For Noise" 
        pn_rayleigh= calculate_rayleigh(mag_noise,'noise_rayleigh'+fname)
        print "Noise: rayleigh distribution parameters: expected= ", pn_rayleigh[0], "var is ", pn_rayleigh[1]
        avg_pn_rayleigh= calculate_rayleigh(avg_noise,'avg_noise_rayleigh'+fname)
        print "Avg Noise: rayleigh distribution parameters: expected= ", avg_pn_rayleigh[0], "var is ", avg_pn_rayleigh[1]

        pn_exponential= calculate_exponential(mag_noise,'noise_exponential'+fname)
        print "Noise: exponential distribution parameters: expected= ", pn_exponential[0], "var ",pn_exponential[1]

        avg_pn_exponential= calculate_exponential(avg_noise,'noise_exponential'+fname)
        print "Avg Noise: exponential distribution parameters: expected= ", avg_pn_exponential[0], "var ",avg_pn_exponential[1]

        
        try:
            print "kl distance: Avg values of noise and signal is=  ", kl_distance(avg_mag,avg_noise)
        except:
            print " dint get the avg signal kl divergence wrt avg noise "
            
        try:
            print "entropy of Noise is= ", kl_distance(mag_noise)
        except:
            print " dint get noise entropy " 

        min_length = min(len(mag_noise), len(mag))
        print " modelled as exponential distribution " 
        error_calculation(min_length, ps_exponential[0], ps_exponential[1], pn_exponential[0], pn_exponential[1],0)
        print "\n \n modelled as rayleigh distribution " 
        error_calculation(min_length, ps_rayleigh[0], ps_rayleigh[1], pn_rayleigh[0], pn_rayleigh[1],1)

if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
