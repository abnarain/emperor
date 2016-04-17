import scipy ,sys, getopt, math
from scipy.fftpack import fft, fftfreq, fftshift
from scipy import signal,arange
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


#matplotlib.pyplot.tight_layout(pad=1.08, h_pad=1.08, w_pad=1.08, rect=1.08)
# Can be used to adjust the border and spacing of the figure
fig_width = 10
fig_length = 10.25
fig_left = 0.12
fig_right = 0.94
fig_bottom = 0.25
fig_top = 0.94
fig_hspace = 0.5

from scipy.signal import butter, lfilter, freqz
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def filereader(filename): 
    z= scipy.fromfile(open(filename), dtype=scipy.complex64)
    # dtype with scipy.int16, scipy.int32, scipy.float32, scipy.complex64 or whatever type you were using.
    mag, phase,x,y = [], [], [], []
    for i in range(0, len(z)):
        mag.append(np.absolute(z[i]))
        x.append(z[i].real)
        y.append(z[i].imag)
        phase.append(np.angle(z[i]))
    return [x,y,mag, phase,z]

def plot_psd(data,fs,filename,flag, clipped):
    # Estimate PSD using Welchs method. Divides the data into overlapping segments, 
    #computing a modified periodogram for each segment and overlapping the periodograms
    plt.figure(figsize=(10,10))
    fig, ax0 = plt.subplots(nrows=1)
    f, Pxx_den = signal.periodogram(data, fs)
    ax0.set_xlabel('frequency [Hz]')
    ax0.set_ylabel('periodogram')
    ax0.plot(f, Pxx_den)
    if flag==1:
       ax0.set_yscale('log')
       ax0.set_ylabel('periodogram (log scale)')
        filename= filename+'_log'
    if clipped :
        ax0.set_xlim(-125*1000, 125*1000)
        filename=filename+'_clipped'
    plt.savefig(filename+'.pdf')

def plot_complex_fft(x, fs, filename, flag, clipped):
    from scipy.fftpack import fft, fftfreq, fftshift
    N=len(x)
    plt.figure(figsize=(10,10))
    fig, ax0 = plt.subplots(nrows=1)
    freqs = fftfreq(N, 1.0/fs)
    freqs = fftshift(freqs)
    yf= 1.0/N *fft(x)
    yf = fftshift(yf)
    ax0.plot(freqs,  np.abs(yf))
    #print "freqs is ", freqs
    #print "FFT vals are",  np.abs(yf)
    ax0.set_xlabel('frequency')
    ax0.set_ylabel('magnitude')
    if flag==1:
        ax0.set_yscale('log')
        ax0.set_ylabel('magnitude (log)')
        filename= filename+'_log'
    if clipped==1 :
        ax0.set_xlim(-125*1000, 125*1000)
        filename=filename+'_clipped'
    plt.savefig(filename+'.pdf',dpi = 110)

def plot_spectrograms(x, fs, filename,nfft,clipped):
    #from matplotlib.colors import BoundaryNorm
    #from matplotlib.ticker import MaxNLocator
    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.
    #cmap = plt.get_cmap('PiYG')
    #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    #im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm)
    #fig.colorbar(im, ax=ax0)
    plt.figure(figsize=(30,15))
    fig, ax1 = plt.subplots(nrows=1)
    from matplotlib import pylab
    Pxx, freqs, time, im = ax1.specgram(x, NFFT=nfft,  Fs=fs, detrend=pylab.detrend_none,
        window=pylab.window_hanning, noverlap=int(nfft * 0.025))
    #ax1.set_xlim(0,1)
    ax1.set_title('specgram spectgm'+'NFFT= %d'%nfft)
    fig.colorbar(im, ax=ax1).set_label("Amplitude (dB)")
    #ax3.axis('tight')
    if clipped :
        ax1.set_ylim(-125*1000,125*1000)
        filename=filename+'_clipped'
    plt.savefig(filename+'.pdf')


def main(argv):
    inputfile=''
    noisefile=''
    noiseflag,inputflag=0,0
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
            inputflag=1
        elif opt in ("-n", "--nfile"):
            noisefile = arg
            noiseflag=1
        else:
            print "check help for usage" 
            sys.exit()

    
    [x,y, mag, phase,z] = filereader(inputfile)
    del x, y, phase
    file1='apr16_code_pf_2MHz'
    fs=2.0* 10**6
    flag=1

    '''
    plt.plot(mag[:500000],'b-')
    plt.savefig('april10_nil_time.pdf')
    sys.exit(1)
    '''

    '''
    order = 6
    cutoff = 100000  # desired cutoff frequency of the filter, Hz
    # Get the filter coefficients so we can check its frequency response.
    b, a = butter_lowpass(cutoff, fs, order)

    # Plot the frequency response.
    w, h = freqz(b, a, worN=8000)
    mag = butter_lowpass_filter(mag, cutoff, fs, order)
    '''

    if inputflag==1:
        print "length of f is ", len(mag)
        #plot_spectrograms(z, fs, file1+'_cspecg_131072',131072,1)
        print "spectrogram for i"
        plot_complex_fft(z, fs, file1+'_cc_fft_131072',1,1)
        plot_psd(z, fs, file1+'_psd_131072',1,1)
        del z
    
    if noiseflag==1:
        [xn,yn,magn,phasen,zn]=filereader(noisefile)
        del xn, yn, phasen
        #magn = butter_lowpass_filter(magn, cutoff, fs, order)
        #print "length of mag is ", len(magn)
        #plot_spectrograms(zn, fs,file2+'_cspecg_131072',131072,1)
        print "spectrogram for n"
        plot_complex_fft(zn, fs, file2+'_cc_fft_131072', 1,1)
        plot_psd(zn,fs, file2+'_psd_131072', 1,1)

if __name__=='__main__':
    main(sys.argv[1:])
