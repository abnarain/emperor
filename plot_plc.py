import scipy ,sys, getopt, math
from scipy.fftpack import fft, fftfreq, fftshift
from scipy import signal,arange
import matplotlib.pyplot as plt
import numpy as np

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

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def give_subplot():
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    return fig

def test_stationarity():
    import statsmodels.api as sm
    test = sm.tsa.adfuller(mag)
    print 'adf: ', test[0]
    print 'p-value: ', test[1]
    print'Critical values: ', test[4]
    if test[0]> test[4]['5%']:
        print "this is stationary"
    else:
        print "not stationary "

def plot_perdiodogram(data,fs,filename,flag):
    f, Pxx_den = signal.periodogram (data, fs)
    fig = give_subplot()
    _subplot= fig.add_subplot(1,1,1)
    _subplot.set_xlabel('frequency [Hz]')
    _subplot.set_ylabel('periodogram')
    _subplot.plot(f, Pxx_den)
    if flag==1:
       _subplot.set_yscale('log')
       filename= filename+'_log'
       _subplot.set_ylabel('periodogram (log scale)')
        
    #data=data[90000:180000]
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename+'.pdf', dpi = 110)

def plot_spectral_density(data,fs,filename,flag):
    # Estimate PSD using Welchs method. Divides the data into overlapping segments, computing a modified periodogram for each segment and overlapping the periodograms
    fig = give_subplot()
    _subplot= fig.add_subplot(1,1,1)
    f, Pxx_den = signal.welch(data, fs)
    _subplot.set_xlabel('frequency [Hz]')
    _subplot.set_ylabel('PSD [V**2/Hz]')
    _subplot.plot(f, Pxx_den)
    if flag==1:
       _subplot.set_yscale('log')
       filename= filename+'_log'
       _subplot.set_ylabel('PSD [V**2/Hz] (log scale) ')

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename+'.pdf', dpi = 110)

def filereader(filename): 
    z= scipy.fromfile(open(filename), dtype=scipy.complex64)
    # dtype with scipy.int16, scipy.int32, scipy.float32, scipy.complex64 or whatever type you were using.
    #z=z[0:1000]
    N=len(z)
    mag, phase,x,y = [], [], [], []
    for i in range(0, len(z)):
        mag.append(np.absolute(z[i]))
        x.append(z[i].real)
        y.append(z[i].imag)
        phase.append(np.angle(z[i]))
    return [x,y,mag, phase,z, N]


def plotSpectrum(y,Fs,filename,flag):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]
    fig = give_subplot()
    _subplot= fig.add_subplot(1,1,1)
    _subplot.plot(frq,abs(Y),'r') # plotting the spectrum
    _subplot.set_xlabel('Freq (Hz)')
    _subplot.set_ylabel('|Y(freq)|')
    if flag==1:
       _subplot.set_yscale('log')
       filename= filename+'_log'
       _subplot.set_ylabel('|Y(freq)| (log scale) ')
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename+'.pdf', dpi = 110)

def plot_fft(x, fs, N, outfile_name,flag):
    '''
    Same as above function to plot the Single sided FFT
    '''
    Fx= fft(x)
    xf = np.linspace(0.0, fs/2.0, N/2)
    fig = give_subplot()
    _subplot = fig.add_subplot(1,1,1)
    _subplot.plot(xf, 2.0/N * np.abs(Fx[0:N/2]))
    _subplot.set_xlabel('frequency')
    _subplot.set_ylabel('magnitude ')
    if flag==1:
       _subplot.set_yscale('log')
       outfile_name= outfile_name+'_log'
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name+'.pdf', dpi = 110)

def plot_complex_fft(x, fs, N, outfile_name, flag):
    yf= fft(x)
    T=1/fs
    xf = fftfreq(N, T)
    xf = fftshift(xf)
    yplot = fftshift(yf)
    fig = give_subplot()
    _subplot = fig.add_subplot(1,1,1)
    _subplot.plot(xf, 1.0/N * np.abs(yf))
    _subplot.set_xlabel('frequency')
    _subplot.set_ylabel('magnitude')
    if flag==1:
        _subplot.set_yscale('log')
        outfile_name= outfile_name+'_log'

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name+'.pdf',dpi = 110)

def plot_hists2(x,y, outfile_name,xlabel='amplitude',ylabel='counts'):
    fig = give_subplot()
    _subplot = fig.add_subplot(1,1,1)
    _subplot.hist(x,color='b', label=xlabel)
    _subplot.hist(y,color='r', label=ylabel, alpha=0.2)
    _subplot.legend()
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name +'.pdf', dpi = 110)

def plot_hists3(x,y,z, outfile_name,xlabel,ylabel,zlabel):
    fig = give_subplot()
    _subplot = fig.add_subplot(1,1,1)
    _subplot.hist(x,color='b', label=xlabel)
    _subplot.hist(y,color='r', label=ylabel, alpha=0.2)
    _subplot.hist(z,color='g', label=zlabel, alpha=0.4)
    _subplot.legend()
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfile_name +'.pdf', dpi = 110)

def plot_hist(mag,filename):
    fig = give_subplot()
    _subplot= fig.add_subplot(1,1,1)
    n, bins, patches = _subplot.hist(mag, 1250, facecolor='green',alpha=0.2)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename+'.pdf', dpi = 110)

def plot_acf_pacf(mag,filename):
    import statsmodels.api as sm
    fig = pyplot.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(mag, lags=2000, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(mag, lags=2005, ax=ax2)
    pyplot.savefig('acf_pacf_2000'+post+'.pdf')

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


def main(argv):
    inputfile=''
    noisefile=''
    noiseflag=0
    try:
        opts, args = getopt.getopt(argv,"h:i:n:",["ifile=","nfile="])
    except getopt.GetoptError:
        print 'file.py -i <inputfile> -n <noisefile>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -i <inputfile> -n <noisefile> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--nfile"):
            noisefile = arg
            noiseflag=1
        else:
            print "check help for usage" 
            sys.exit()

    mag=[]
    
    [x,y, mag, phase,z, Ns] = filereader(inputfile)
    del x, y, phase
    l=inputfile.split('_')
    print "\nthe elements are: ", l
    filename= '_'.join([ l[1][-4:] ,l[2],l[3]])
    print "input file is",inputfile
    print "length of f is ", len(mag)
    fs=200* math.pow(10,3)
    flag=1
    print "sampling frequency is ",fs
    plot_hist(mag,filename+'hist_1250')
    plotSpectrum(z,fs,filename+'_fft',flag)
    plot_perdiodogram(z,fs,filename+'_periodogram',flag)
    plot_complex_fft(z, fs, Ns, filename+'_cc_fft', flag)
    print "Hurst(data's magnitude)index of :   %s" % hurst(mag)
    #plot_spectral_density(z,fs,filename+'_welch_psd',flag) #averaged
    if noiseflag==1:
        [xn,yn,magn,phasen,zn,Nsn]=filereader(noisefile)
        plot_hist(magn,filename+'hist_noise_1250')
        plotSpectrum(magn,fs,filename+'noise_fft',flag)
        plot_perdiodogram(zn,fs,filename+'noise_periodogram',flag)
        plot_complex_fft(zn, fs, Nsn, filename+'noise_cc_fft', flag)
        plot_hists2(mag,magn, filename+'noise_data_',xlabel='amplitude',ylabel='counts')


if __name__=='__main__':
    main(sys.argv[1:])
