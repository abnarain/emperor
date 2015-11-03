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
        opts, args = getopt.getopt(argv,"h:i:f::o",["ifile=","ftype=","ofile"])
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
        elif opt in ("-o", "--ftype"):
            compare_file = arg
        else:
            print "check help for usage" 
            sys.exit()


    f = scipy.fromfile(open(inputfile), dtype=scipy.float32)
    false_positives, false_negatives=0,0
    negative =1;
    if negative ==1:
        for i in range(0,len(f)):
            if f[i] == 0.0 :
                false_negatives += 1
    elif negative ==0:
        for i in range(0,len(f)):
            if f[i] == 1.0 :
                false_positives += 1
    print "false negatives ",false_negatives, len(f), false_negatives*1.0/len(f)
    print "false positives ",false_positives, len(f), false_positives*1.0/len(f)
    #plotter(measured_data,[], "measured_data.pdf","plotting the data","index","y value")

if __name__=='__main__':
    main(sys.argv[1:])
