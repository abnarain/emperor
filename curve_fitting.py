import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
from scipy.stats import norm,rayleigh, expon, entropy
import sys, scipy, getopt, pylab
import numpy as np

import matplotlib.font_manager
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


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
        pdf_fitted1 = rayleigh.pdf(i,loc=param_s1,scale=param_s2) # fitted distribution
        pdf_fitted2 = rayleigh.pdf(i,loc=param_n1,scale=param_n2) # fitted distribution\
    elif flag==0:
        pdf_fitted1 = expon.pdf(i,loc=param_s1,scale=param_s2) # fitted distribution
        pdf_fitted2 = expon.pdf(i,loc=param_n1,scale=param_n2) # fitted distribution\


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
    if qk != None:
        min_len = min(len(pk),len(qk))
        return entropy(pk[:min_len], qk[:min_len])
    else:    
        return entropy(pk, qk)



def plot_hist(data,filename,flag,data2=None):
    fig2 = Figure(linewidth=0.0)
    fig2.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig2, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot2 = fig2.add_subplot(1,1,1)
    _subplot2.hist(data, bins=1200, normed=True,alpha=0.3)
    if not (data2 ==None):
        _subplot2.hist(data2, bins=1200, normed=True,alpha=0.5)
    if flag==1:
        _subplot2.set_xscale('log')
        filename+'_log'

    canvas = FigureCanvasAgg(fig2)
    canvas.print_figure(filename+'.pdf', dpi = 110)

def curve_fitting_exp(x,a,b,c):
    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    x = np.linspace(0,4,50)
    y = func(x, 2.5, 1.3, 0.5)
    yn = y + 0.2*np.random.normal(size=len(x))

    popt, pcov = curve_fit(func, x, yn)
    return popt

def calculate_exponential(data,outfile_name):
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1) #, bins, patches = pyplot.hist(mag, 1250, facecolor='green')
    bins, events, patches=  _subplot.hist(data,bins=1200,normed=1) 
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name+'_hist.pdf', dpi = 110)

    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot1 = fig1.add_subplot(1,1,1)
    param = expon.fit(data) # distribution fitting - location, scale - mean and MLE estimator 
    print "parameters are " ,param
    pdf_fitted = expon.pdf(events,loc=param[0],scale=param[1]) # fitted distribution
    print "Exponential: pdf fitted ", pdf_fitted
    _subplot1.plot(pdf_fitted)
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(exp_+'_pdf_fitted.pdf', dpi = 110)

    return param

def calculate_rayleigh(data,outfile_name):
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1) #, bins, patches = pyplot.hist(mag, 1250, facecolor='green')
    bins, events, patches=  _subplot.hist(data,bins=1200,normed=1) 
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name+'_hist.pdf', dpi = 110)

    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot1 = fig1.add_subplot(1,1,1)
    param = expon.fit(data) # distribution fitting - location, scale - mean and MLE estimator 
    print "Rayleigh: parameters are " ,param
    pdf_fitted = expon.pdf(events,loc=param[0],scale=param[1]) # fitted distribution
    print "pdf fitted ", pdf_fitted
    _subplot1.plot(pdf_fitted)
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(fog+'_pdf_fitted.pdf', dpi = 110)
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

    mag, mag_noise, avg_mag, avg_noise=[],[], [], []
    data= scipy.fromfile(open(inputfile), dtype=scipy.complex64)
    for i in range(0,len(data)):
        mag.append(np.absolute(data[i]))

    #avg_mag=movingaverage(mag ,100)
    #ps_rayleigh= calculate_rayleigh(mag,'signal_rayleigh')
    #print "Signal: rayleigh distribution parameters: expected= ", ps_rayleigh[0], "var is ", ps_rayleigh[1]

    #ps_exponential= calculate_exponential(mag,'signal_exponential')
    #print "Signal: exponential distribution parameters: expected= ", ps_exponential[0], "var ",ps_exponential[1]
    #ps = expected_value(mag)
    #print "Signal: expected value acc to time series (E(yy*))  ", ps
    #print "entropy of signal is= ", kl_distance(mag)

    if noiseflag==1:
        noise= scipy.fromfile(open(noisefile), dtype=scipy.complex64)
        for i in range(0,len(noise)):
            mag_noise.append(np.absolute(noise[i]))
        
        avg_noise=movingaverage(mag_noise ,100)
        #print "For Noise" 
        #pn_rayleigh= calculate_rayleigh(mag_noise,'noise_rayleigh')
        #print "Noise: rayleigh distribution parameters: expected= ", pn_rayleigh[0], "var is ", pn_rayleigh[1]

        #pn_exponential= calculate_exponential(mag_noise,'noise_exponential')
        #print "Noise: exponential distribution parameters: expected= ", pn_exponential[0], "var ",pn_exponential[1]

        #pn = expected_value(mag_noise)
        #print "Noise: Expected value acc to time series (E(nn*)) ", pn
        
        #print "the kl distance between th enoise and the signal is=  ", kl_distance(mag,mag_noise)
        #print "entropy of Noise is= ", kl_distance(mag_noise)

        #min_length = min(len(mag_noise), len(mag))
        #print " modelled as exponential distribution " 
        #error_calculation(min_length, ps_exponential[0], ps_exponential[1], pn_exponential[0], pn_exponential[1],0)
        #print "\n \n modelled as rayleigh distribution " 
        #error_calculation(min_length, ps_rayleigh[0], ps_rayleigh[1], pn_rayleigh[0], pn_rayleigh[1],1)


        min_length = min(len(mag_noise), len(mag))
        min_length_avg = min(len(mag_noise), len(mag))
        plot_hist(mag[:min_length],'combined',1,data2=mag_noise[:min_length])
        #plot_hist(avg_mag[:min_length_avg],'avg_combined',1,data2=avg_noise[:min_length_avg])
        plot_hist(mag[:min_length],'combined',0,data2=mag_noise[:min_length])
        #plot_hist(avg_mag[:min_length_avg],'avg_combined',0,data2=avg_noise[:min_length_avg])

if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
