import numpy as np
import scipy, sys, getopt
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import pyplot



fig_width = 10
fig_length = 10.25
# Can be used to adjust the border and spacing of the figure
fig_left = 0.12
fig_right = 0.94
fig_bottom = 0.25
fig_top = 0.94
fig_hspace = 0.5

def counting_preamble(f):
    print "length of f is ", len(f)
    count_2,count_0,count_1=0,0,0
    for i in range(92550,100520):
        if f[i]==2.0:
            count_2 +=1
        elif f[i]==0.0:
            count_0 +=1
        elif f[i]==1.0:
            count_1 +=1
        else:
            print "there is something I donno", f[i]

    print "0 is", count_0
    print "1 is", count_1
    print "2 is", count_2

def plotter(x,y, outfile_name,title,xlabel,ylabel):
    fig = Figure(linewidth=0.0)
    fig.set_size_inches(fig_width,fig_length, forward=True)
    Figure.subplots_adjust(fig, left = fig_left, right = fig_right, bottom = fig_bottom, top = fig_top, hspace = fig_hspace)
    _subplot = fig.add_subplot(1,1,1)
    _subplot.plot(x, label=xlabel)
    _subplot.legend()
    _subplot.set_title(title,fontsize=17)
    canvas = FigureCanvasAgg(fig)
    if '.pdf' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)
    if '.png' in outfile_name:
        canvas.print_figure(outfile_name, dpi = 110)


def just_plot(f):
    pyplot.plot(f,'o-')
    pyplot.ylim(-1,3)
    pyplot.legend()
    pyplot.show()



def main(argv):
    inputfile=''
    ftype=''
    compare_file=''
    try:
        opts, args = getopt.getopt(argv,"h:i:f:o:",["ifile=","ftype=","ofile="])
    except getopt.GetoptError:
        print 'file.py -i <inputfile> -f <caption on graph>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -i <inputfile> -o <compare_file> -f <caption on graph> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-f", "--ftype"):
            ftype = arg
        elif opt in ("-o", "--ofile"):
            compare_file = arg
        else:
            print "check help for usage" 
            sys.exit()

    
    f = scipy.fromfile(open(inputfile), dtype=scipy.float32)
    c_whole = scipy.fromfile(open(compare_file), dtype=scipy.float32)
    print "\n lengths for measured data:" , len(f), "length of orig transmission: ",len(c_whole)
    preamble = [1,0,0,1,0,0,1,0,0,1,0,0]*200
    #for i in range(0, len(f)):
    # Take bits as a 0 
    cor1 = np.correlate(f,preamble,'full')
    collected_array=[]
    maximum=0
    for i in range(0,len(cor1)):
        if cor1[i] > maximum :
            maximum=int(cor1[i])

    for i in range(0,len(cor1)):
        if cor1[i] > maximum or cor1[i]==maximum:            
            collected_array.append(cor1[i])
    m=np.median(collected_array)
    print "value of the mean index is ", m
    index = m-len(preamble)/2
    start_data_index = m+len(preamble)/2
    print "index = ",index, "start data index = ", start_data_index
    c=c_whole[len(preamble):]
    measured_data= f[start_data_index:start_data_index+ len(c) ]
    xored_data =[]
    false_positives, false_negatives =0, 0
    print "length of c= ", len(c)
    print "length measured_data ", len(measured_data)
    max_len= min(len(measured_data), len(c))
    for i in range(0,max_len):
        xored_data.append(int(measured_data[i]) ^ int(c[i]))
        if c[i] == 0.0 and  measured_data[i] == 1.0 : 
            false_positives += 1
        if c[i] == 1.0 and  measured_data[i] == 0.0 : 
            false_negatives += 1

    errors = sum(xored_data)
    bit_error_rate= errors*1.0/len(xored_data)
    print "whole length of message/xored_data", len(xored_data), "length of orig message ", len(c)
    print " bit error rate with xored_length ", bit_error_rate
    print " bit error rate with orig message length", errors*1.0/len(c)
    print "false negatives ", false_negatives
    print "false positives ", false_positives
    #plotter(measured_data,[], "measured_data.pdf","plotting the data","index","y value")
    #plotter(f[117000:138000],[], "autoc.pdf","correlation","auto index","y value")


if __name__=='__main__':
    main(sys.argv[1:])
