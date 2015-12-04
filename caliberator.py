import scipy, sys, getopt, pickle
from scipy.stats import norm,rayleigh, expon, entropy
import numpy as np



def movingaverage(interval, window_size=512):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def distribution_statistic(data,bins):
    try :
        rayleigh_param = rayleigh.fit(data)
    except:
        print "screwed raleigh fit "
    print "params for rayleigh " ,rayleigh_param

    try:
        pdf_rayleigh_fitted = rayleigh.pdf(bins, *rayleigh_param[:-2],loc=rayleigh_param[0],scale=rayleigh_param[1]) # fitted distribution
    except :
        print " returning as nothing to plot rayleigh "

    try :
        exp_param = expon.fit(data)
    except:
        print "screwed expon fit "
    print "params for exponential ", exp_param

    try:
        pdf_exp_fitted = expon.pdf(bins, *exp_param[:-2],loc=exp_param[0],scale=exp_param[1]) # fitted distribution
    except :
        print " returning as nothing to plot exponential" 
    return [exp_param, pdf_exp_fitted, rayleigh_param, pdf_rayleigh_fitted]

def main(argv):
    noisefile=''
    onesfile=''
    pmode,noiseflag,onesflag=0,0,0
    
    try:
        opts, args = getopt.getopt(argv,"h:n:o:p:",["nfile=","ofile=","pmode="])
    except getopt.GetoptError:
        print 'file.py -i <noisefile> -o <onesfile>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -n <noisefile> -o <onesfile> '
            sys.exit()
        elif opt in ("-n", "--nfile"):
            noisefile = arg
            noiseflag=1
        elif opt in ("-o", "--ofile"):
            onesfile = arg
            onesflag =1
        elif opt in ("-p", "--pmode"):
            pmode= 1
        else:
            print "check help for usage" 
            sys.exit()
    if pmode ==1:
        nl=noisefile.split('_')
        Noisepickle= '_'.join([ nl[-4][-5:], nl[-3][-2:], nl[-2], nl[-1][:-4]])    
        ol=onesfile.split('_')
        Onespickle= '_'.join([ ol[-4][-4:], ol[-3][-2:], ol[-2], ol[-1][:-4]])
        if noiseflag ==1:
            z_noise= scipy.fromfile(open(noisefile), dtype=scipy.complex64)
            noise=map(np.absolute,z_noise)
            noise_hist, noise_bins= np.histogram(noise,200,density=1)
            [noise_exp_param, noise_pdf_exp_fitted, noise_rayleigh_param, noise_pdf_rayleigh_fitted] = distribution_statistic(noise, noise_bins)
            pickle.dump([noise_exp_param, noise_pdf_exp_fitted, noise_rayleigh_param, noise_pdf_rayleigh_fitted], open(Noisepickle+'.pickle','wb'))
        if onesflag ==1:
            z_ones= scipy.fromfile(open(onesfile), dtype=scipy.complex64)
            ones=map(np.absolute,z_ones)
            ones_hist, ones_bins= np.histogram(ones,200,density=1)
            [ones_exp_param, ones_pdf_exp_fitted, ones_rayleigh_param, ones_pdf_rayleigh_fitted] = distribution_statistic(ones, ones_bins)
            pickle.dump([ones_exp_param, ones_pdf_exp_fitted, ones_rayleigh_param, ones_pdf_rayleigh_fitted], open(Onespickle+'.pickle','wb'))

        print "Done with Pickle mode "
        sys.exit(1)

    false_positives, false_negatives=0,0
    
    if noiseflag ==1:
        print " Noise caliberation "
        noise= scipy.fromfile(open(noisefile), dtype=scipy.float32)
        for i in range(0,len(noise)):
            if noise[i] == 1.0 :
                false_positives += 1
        print "false positives ",false_positives, len(noise), false_positives*1.0/len(noise)
    if onesflag==1:
        print "Training caliberation "
        ones= scipy.fromfile(open(onesfile), dtype=scipy.float32)
        for i in range(0,len(ones)):
            if ones[i] == 0.0 :
                false_negatives += 1
        print "\nfalse negatives ",false_negatives, len(ones), false_negatives*1.0/len(ones)

if __name__=='__main__':
    main(sys.argv[1:])


