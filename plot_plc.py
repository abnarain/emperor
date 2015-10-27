import scipy
from scipy.fftpack import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
import numpy as np
import sys, getopt

import matplotlib.font_manager
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


def plot_perdiodogram(data,fs, outfile_name):

    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)

    f, Pxx_den = signal.periodogram (data, fs)    
    _subplot.set_xlabel('frequency [Hz]')
    _subplot.set_ylabel('periodogram')
    _subplot.set_yscale('log')
    #_subplot.semilogy(f, Pxx_den)
    #pyplot.ylim([0.5e-3, 1])

    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    

def plot_specral_density(data,fs, outfile_name):    
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)

    f, Pxx_den = signal.welch(data, fs)
    _subplot.set_xlabel('frequency [Hz]')
    _subplot.set_ylabel('PSD [V**2/Hz]')
    _subplot.set_yscale('log')
    #_subplot.semilogy(f, Pxx_den)
    #pyplot.ylim([0.5e-3, 1])
    #pyplot.show()

    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)

    
def plot_hist(mag,title, xlabel, outfile_name):
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.hist(mag, 1250, color='b', label=xlabel)
    _subplot.legend()
    _subplot.set_title(title,fontsize=17)

    #n, bins, patches = pyplot.hist(mag, 1250, facecolor='green')
    _subplot.set_xlim((0,.018))

    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)

   
def hurst(ts):
    from numpy import cumsum, log, polyfit, sqrt, std, subtract
    """Returns the Hurst Exponent of the time series vector ts"""
    # Create the range of lag values
    lags = range(2, 20000)
    # Calculate the array of the variances of the lagged differences
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    # Use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    #Create a Gometric Brownian Motion, Mean-Reverting and Trending Series
    #gbm = log(cumsum(randn(100000))+1000)
    #mr = log(randn(100000)+1000)
    #tr = log(cumsum(randn(100000)+1)+1000)
    return poly[0]*2.0

def plot_acf_pacf(mag, title, xlabel, outfile_name):
    import statsmodels.api as sm
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.hist(mag, 1250, color='b', label=xlabel)
    _subplot.legend()
    _subplot.set_title(title,fontsize=17)

    fig = sm.graphics.tsa.plot_acf(mag, lags=20000 , ax=_subplot)
    #ax2 = fig.add_subplot(212)
    #fig = sm.graphics.tsa.plot_pacf(mag, lags=2005, ax=ax2)
    #pyplot.show()

    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)


def filereader(filename): 
    z= scipy.fromfile(open(filename), dtype=scipy.complex64)
    # dtype with scipy.int16, scipy.int32, scipy.float32, scipy.complex64 or whatever type you were using.
    #z=z[0:100]
    N=len(z)
    mag, phase,x,y = [], [], [], []
    for i in range(0, len(z)):
        mag.append(np.absolute(z[i]))
        x.append(z[i].real)
        y.append(z[i].imag)
        phase.append(np.angle(z[i]))
    return [x,y,mag, phase,z, N]
                                                                            
def plot_fft(x, fs, N, outfile_name, title ):
    Fx= fft(x)
    xf = np.linspace(0.0, fs/2.0, N/2)
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.plot(xf, 2.0/N * np.abs(Fx[0:N/2]))
    _subplot.set_xlabel('frequency')
    _subplot.set_ylabel('magnitude (log) ')
    _subplot.set_yscale('log')
    _subplot.set_title(title,fontsize=17)
    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
         canvas.print_figure(outfile_name, dpi = 110)

def plot_complex_fft(x, fs, N, outfile_name, title ):
    yf= fft(x)
    T=1/fs
    xf = fftfreq(N, T)
    xf = fftshift(xf)
    yplot = fftshift(yf)
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.plot(xf, 1.0/N * np.abs(yf))
    _subplot.set_xlabel('frequency')
    _subplot.set_ylabel('magnitude')# (log) ')
    #_subplot.set_yscale('log')
    _subplot.set_title(title,fontsize=17)
    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)

def hists(x,y, outfile_name,title,xlabel,ylabel):
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.hist(x,color='b', label=xlabel)
    _subplot.hist(y,color='r', label=ylabel, alpha=0.5)
    _subplot.legend()
    _subplot.set_title(title,fontsize=17)
    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)

def main1(argv):
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
    print "input file is " , inputfile, ftype
    [x,y, mag, phase,z, Ns] = filereader(inputfile)
    fs=1e6
    hists(x,y, 'xAndy_'+ftype+'.png', 'x and y values of Noise '+ftype, 'x value', 'y value')
    hists(mag,phase, 'magAndphase_'+ftype+'.png', 'magnitude and phase of Noise '+ftype, 'magnitude value', 'phase value')
    plot_complex_fft(z,fs, Ns,'fft_complex_'+ftype+'.pdf','Noise (complex) in '+ ftype)

    #plot_fft(x,fs,Ns,'fft_x_log_'+ ftype+'.pdf','x value of Noise in '+ ftype)
    #plot_fft(y,fs, Ns,'fft_y_log_'+ftype+'.pdf','y value of Noise in '+ftype )
    #plot_fft(mag,fs, Ns,'fft_mag_log_'+ftype+'.pdf', 'magnitude of Noise in '+ftype)
    # 
    #plot_fft(phase,fs, Ns,'fft_phase_log_'+ftype+'.pdf', 'phase of Noise in '+ ftype)
    # To plot FFT on log scale
    #plot_complex_fft(z,fs, Ns,'fft_complex_log_'+ftype+'.pdf','Noise (complex) in '+ ftype)

def main2(argv):
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
    #data=data[90000:180000]
    print "length of f is ", len(data)
    for i in range(0,len(data)):
        mag.append(np.absolute(data[i]))
    import math
    fs=200* math.pow(10,3)
    print "sampling frequency is ",fs
    #plot_perdiodogram(data,fs)
    #plot_specral_density(data,fs)
    #plotSpectrum(data,fs)
    plot_hist(mag, "histogram of Noise magnitude", "Noise magnitude", ftype)
    #plot_acf_pacf(mag,"ACF of noise magnitude","distribution of noise magnitude", ftype)
    #print "Hurst(data's magnitude) inddex is :   %s" % hurst(mag)






if __name__=='__main__':
    main2(sys.argv[1:])
