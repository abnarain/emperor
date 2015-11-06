import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import numpy as np
import scipy, sys, getopt,struct,reedsolo
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

#this takes the data got from Gnuradio contaning the message and then calculates the errors that occur following the preamble attached to the message #It also gets the actual bitstream to be shoved into RS decoder to get the ascii message transmitted on the first go.

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
    canvas.print_figure(outfile_name, dpi = 110)

def error_rate_calculations(to_decode_data, original_message):
    xored_data =[]
    false_positives, false_negatives =0, 0
    print "length to_decode_data ", len(to_decode_data), "len of c",len(original_message)
    max_len= min(len(to_decode_data), len(original_message))
    for i in range(0,max_len):
        xored_data.append(int(to_decode_data[i]) ^ int(original_message[i]))
        if original_message[i] == 0.0 and  to_decode_data[i] == 1.0 : 
            false_positives += 1
        if original_message[i] == 1.0 and  to_decode_data[i] == 0.0 : 
            false_negatives += 1

    errors = sum(xored_data)
    bit_error_rate= errors*1.0/len(xored_data)
    print "whole length of message/xored_data", len(xored_data), "length of orig message ", len(original_message)
    print " bit error rate with xored_length ", bit_error_rate
    print " bit error rate with orig message length", errors*1.0/len(original_message)
    print "false negatives ", false_negatives
    print "false positives ", false_positives

preamble = [1,0,0,1,0,0,1,0,0,1,0,0]*200
def start_index(to_decode_file):
    cor1 =  np.correlate(to_decode_file,preamble,"full")
    cor2 =  np.correlate(preamble,preamble,"full")
    collected_array=[]
    maximum=0
    for i in range(0,len(cor1)):
        if cor1[i] > maximum :
            maximum=int(cor1[i])

    for i in range(0,len(cor1)):
        if  cor1[i]==maximum:            
            collected_array.append(i)
    m= min(collected_array)
    get_index=0
    for i in range(0,len(cor2)):
        if m>cor2[i]:
            get_index=i
            print "max correlation index ",get_index
            break
    print "value of the mean index is ", m, "max correlation is", maximum
    return [get_index,m]

def decoding_byte_array(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64) 
        d=to_decode_data[idx]
        if tup[1]==101:
            if to_decode_data[idx ]==1 and to_decode_data[idx+1]==0 and to_decode_data[idx+2]==1:
               rs_decoder_input.append('0')
               print "adding 101"
        if tup[1]==11 :
            if to_decode_data[idx ]==1 and to_decode_data[idx+1] ==1:
                rs_decoder_input.append('1')
                print "adding 11 "

    print len(rs_decoder_input)*1.0/8 , " this must be a number"
    rs_feed=''.join(rs_decoder_input)
    bin_rep_to_decode = bytearray()
    #print "length of rs feed is ",len(rs_feed)
    #print "rs feed string is " ,rs_feed
    for i in range(0,len(rs_feed),8):
        x= rs_feed[i:i+8]
        sx=struct.pack('B',int(x,2))
        bin_rep_to_decode.extend(sx)

    return bin_rep_to_decode

def main(argv):
    inputfile=''
    ftype=''
    original_file=''
    try:
        opts, args = getopt.getopt(argv,"h:d:i:o:",["dfile=","itype=","ofile="])
    except getopt.GetoptError:
        print 'file.py -d <file_to_decode>  -o <original_file>  -i <indices_file>'
        sys.exit(2)
    for opt, arg in opts:
        print opt ,arg,
        if opt == '-h':
            print 'file.py -d <file_to_decode>  -o <original_file> -i <indices_file> '
            sys.exit()
        elif opt in ("-d", "--dfile"):
            inputfile = arg
        elif opt in ("-i", "--itype"):
            indices_file = arg
        elif opt in ("-o", "--ofile"):
            original_file = arg
        else:
            print "check help for usage" 
            sys.exit()

    to_decode_file = scipy.fromfile(open(inputfile), dtype=scipy.float32)
    original_string = scipy.fromfile(open(original_file), dtype=scipy.float32)
    oracle_indices = np.load(indices_file)
    to_decode_file=original_string
    print "\n lengths for measured data:" , len(to_decode_file), "length of orig transmission: ",len(original_string)
    [get_index,m ]=start_index(to_decode_file)
    index = m -(len(preamble)-get_index)+1
    start_data_index = index+(len(preamble)-get_index)
    original_message =original_string[len(preamble):]
    to_decode_data= original_string
    to_decode_data1= to_decode_file[start_data_index: start_data_index+len(original_message) ]
    to_decode_data= to_decode_data1.astype(np.int64)
    plt.plot(to_decode_file[index:start_data_index+get_index])
    plt.savefig('first.pdf')
    plt.plot(to_decode_data)
    plt.savefig('second.pdf')
    bin_rep_to_decode=decoding_byte_array(oracle_indices,to_decode_data)
    print "Going to decode"
    rs= reedsolo.RSCodec(32)
    message_decoded = rs.decode(bin_rep_to_decode)
    print "decoded message is ",message_decoded
    print "\n"

if __name__=='__main__':
    main(sys.argv[1:])
