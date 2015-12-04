import scipy, sys, getopt

def main(argv):
    noise_file=''
    ones_file=''
    noiseflag,onesflag=0,0
    try:
        opts, args = getopt.getopt(argv,"h:n:o",["nfile=","ofile="])
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
            noiseflag =1
        else:
            print "check help for usage" 
            sys.exit()

    false_positives, false_negatives=0,0
    negative =0

    if noiseflag ==1:
        print " Noise caliberation "
        noise= scipy.fromfile(open(onesfile), dtype=scipy.float32)
        for i in range(0,len(noise)):
            if noise[i] == 1.0 :
                false_positives += 1
        print "false positives ",false_positives, len(f), false_positives*1.0/len(f)
    if onesflag==1:
        print "Training caliberation "
        ones= scipy.fromfile(open(onesfile), dtype=scipy.float32)
        for i in range(0,len(ones)):
            if f[i] == 0.0 :
                false_negatives += 1
        print "\nfalse negatives ",false_negatives, len(f), false_negatives*1.0/len(f)


if __name__=='__main__':
    main(sys.argv[1:])
