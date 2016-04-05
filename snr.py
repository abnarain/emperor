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

preamble=[1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,1,0,1,0,1]

def snr_est_simple(signal):
    s = scipy.mean(abs(signal)**2)
    n = 2*scipy.var(abs(signal))
    snr_rat = s/n
    return 10.0*scipy.log10(snr_rat), snr_rat

def snr_est_skew(signal):
    y1 = scipy.mean(abs(signal))
    y2 = scipy.mean(scipy.real(signal**2))
    y3 = (y1*y1 - y2)
    y4 = online_skewness(signal.real)
    #y4 = stats.skew(abs(signal.real))

    skw = y4*y4 / (y2*y2*y2);
    s = y1*y1
    n = 2*(y3 + skw*s)
    snr_rat = s / n
    return 10.0*scipy.log10(snr_rat), snr_rat

def snr_est_m2m4(signal):
    M2 = scipy.mean(abs(signal)**2)
    M4 = scipy.mean(abs(signal)**4)
    snr_rat = scipy.sqrt(2*M2*M2 - M4) / (M2 - scipy.sqrt(2*M2*M2 - M4))
    return 10.0*scipy.log10(snr_rat), sn

def snr_est_svr(signal):
    N = len(signal)
    ssum = 0
    msum = 0
    for i in xrange(1, N):
        ssum += (abs(signal[i])**2)*(abs(signal[i-1])**2)
        msum += (abs(signal[i])**4)
    savg = (1.0/(float(N)-1.0))*ssum
    mavg = (1.0/(float(N)-1.0))*msum
    beta = savg / (mavg - savg)

    snr_rat = ((beta - 1) + scipy.sqrt(beta*(beta-1)))
    return 10.0*scipy.log10(snr_rat), snr_rat


# You can compare the log likelihood distance of distributions
# You can compare the mean == That is the expectation of the value (E[nn*])
# You can compare the expectaton using the values in the curve estimated 

_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64
def hellinger3(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


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


def approximating_dists(data,bins):
    try :
        exp_param = expon.fit(data)
    except:
        print "screwed expon fit "
    #print "params for exponential ", exp_param

    try:
        pdf_exp_fitted = expon.pdf(bins, *exp_param[:-2],loc=exp_param[0],scale=exp_param[1]) # fitted distribution
    except :
        print " returning as nothing to plot "
    return [exp_param, pdf_exp_fitted]

def start_index(to_decode_file):
    cor1 =  np.correlate(to_decode_file,preamble,"full")
    maximum=max(cor1)
    min_index_of_max=0
    for i in range(0,len(cor1)):
        if  cor1[i]==maximum:
            min_index_of_max= i
            break
    return min_index_of_max


def main(argv):
    msg_ook_file,noise_iq_file,msg_iq_file='','',''
    print " main "
    try:
        opts, args = getopt.getopt(argv,"h:m:y:n::",["mfile=","miqfile","niqfile="])
    except getopt.GetoptError:
        print 'file.py -m <msg file> -n <noise iq file> -y <msg iq file>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -m <msg file> -n <noise iq file> -y <msg iq file>'
            sys.exit()
        elif opt in ("-m", "--mfile"):
            msg_ook_file = arg
        elif opt in ("-y", "--miqfile"):
            msg_iq_file = arg
        elif opt in ("-n", "--niqfile"):
            noise_iq_file = arg
        else:
            print "check help for usage" 
            sys.exit()



    msg_bit_size=896#write logic for _7 
    file_parts=msg_ook_file.split('_')
    print file_parts
    file_parts[-1]= 'iq.dat'
    msg_iq_file = '_'.join(file_parts)
    file_parts.remove('04')
    #file_parts[-3]  ='feb164/noise' Use this 
    #file_parts[-3][-4:]  ='noise'
    file_parts[-3]  ='noise'
    noise_iq_file='_'.join(file_parts)
    print noise_iq_file
    print msg_iq_file
    
    ook_data= scipy.fromfile(open(msg_ook_file), dtype=scipy.float32)
    get_index=start_index(ook_data)
    start_data_index = get_index +1
    to_decode_data= ook_data[start_data_index:]
    exp_mean_diff, kl_exp, h_exp, d_exp_sq_err, d_exp_l1=-1,-1,-1,-1,-1 
    ray_mean_diff, kl_ray, h_ray, d_ray_sq_err, d_ray_l1=-1,-1,-1,-1,-1

    msg_iq_data= scipy.fromfile(open(msg_iq_file), dtype=scipy.complex64)
    msg_mod  =map(np.absolute,msg_iq_data)
    msg_mag = map(lambda x: x**2, msg_mod)

    noise_iq_data= scipy.fromfile(open(noise_iq_file), dtype=scipy.complex64)
    noise_mod=map(np.absolute,noise_iq_data)
    noise_mag=map(lambda x: x**2, noise_mod)

    l=msg_ook_file.split('_')
    #print "\nl is ", l
    #print "\nthe elements are: ", l[-3][-2:], l[-2], l[-1]
    fname= '_'.join(['curve',l[-4][-2:], l[-3][-2:] , l[-2]])
    print "filename is " , fname

    samples_per_symbol=10
    pr_start_iq_idx=(start_data_index)*samples_per_symbol
    pr_end_iq_idx=(start_data_index+msg_bit_size**2)*samples_per_symbol  #print "starting of data is  ", start_data_index

    msg_iq_data= msg_iq_data[pr_start_iq_idx:pr_end_iq_idx]
    msg_mod  =map(np.absolute,msg_iq_data)
    data_samples = map(lambda x: x**2, msg_mod)

    noise_iq_data= noise_iq_data[pr_start_iq_idx:pr_end_iq_idx]
    noise_mod=map(np.absolute,noise_iq_data)
    noise_samples=map(lambda x: x**2, noise_mod)

    
    noise_samples=noise_mag[pr_start_iq_idx:pr_end_iq_idx]
    
    data_hist, data_bins= np.histogram(data_samples,200,density=1)
    [d_exp_param, d_pdf_exp_fitted] = approximating_dists(data_samples,data_bins)

    noise_hist, noise_bins= np.histogram(noise_samples,200,density=1)
    [n_exp_param, n_pdf_exp_fitted]= approximating_dists(noise_samples, noise_bins)

    fig1 = Figure(linewidth=0.0)
    fig1.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig1, left = fig_left, right = fig_right, bottom =
    fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig1.add_subplot(1,1,1)
    
    #print "data exp param ",d_exp_param, "data rayleigh param ", d_rayleigh_param
    _subplot.hist(data_samples,200,facecolor='red', alpha=0.6, normed=1, label= 'data')
    _subplot.hist(noise_samples,200,normed=1,alpha=0.5, facecolor='blue', label='noise')

    #_subplot.plot(data_bins,d_pdf_rayleigh_fitted,'r-',label='data estimate rayleigh')
    _subplot.plot(data_bins,d_pdf_exp_fitted,'r-', label='data estimate exp')
    _subplot.plot(noise_bins,n_pdf_exp_fitted,'b-', label='noise estimate exp')
    
    kl_exp,sig_power,noise_power=-1,-1,-1
    #print "KL Divergence of data wrt noise(exp) ", 
    kl_exp=kl_distance(n_pdf_exp_fitted, d_pdf_exp_fitted)
    #h_exp= hellinger3(n_pdf_exp_fitted, d_pdf_exp_fitted)
    #print "\n modelled as exponential distribution "
    
    snr= snr_est_svr(msg_iq_data)
    try:
        sig_power=2*scipy.var(abs(msg_iq_data))
    except:
        print "no sig power"
    try:    
        noise_power=2*scipy.var(abs(noise_iq_data))
    except:
        print "no noise power"
    #print "\n modelled as rayleigh distribution "
    print kl_exp, snr, sig_power, noise_power

    #_subplot.set_xlim(0,xlim)
    #_subplot.legend()
    canvas = FigureCanvasAgg(fig1)
    canvas.print_figure(fname+'.pdf', dpi = 110)


if __name__=='__main__':
    print "in main"
    main(sys.argv[1:])
