#This decoder basically produces a different decoder approach than decoder.py 
#as there is problem with perfect synchronization of data . Implements a FSM
#kind of approach and forgets the number of zeros emitted in between
#look at decoder_array3 for exactly what's done
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
    assert(len(to_decode_data)==len(original_message))
    for i in range(0,len(to_decode_data)):
        xored_data.append(int(to_decode_data[i]) ^ int(original_message[i]))
        if original_message[i] == 0 and  to_decode_data[i] == 1 : 
            false_positives += 1
        if original_message[i] == 1 and  to_decode_data[i] == 0 : 
            false_negatives += 1

    original_message = [2*i for i in original_message]
    plt.plot(to_decode_data[:1200],'g',label="decoded data")
    plt.plot(original_message[:1200], 'b',alpha=0.4,label="original data")
    plt.savefig("seethetruth.pdf")
    errors = sum(xored_data)
    bit_error_rate= errors*1.0/len(xored_data)
    print "whole length of message/xored_data", len(xored_data), "length of orig message ", len(original_message)
    print " bit error rate with xored_length ", bit_error_rate
    print " bit error rate with orig message length", errors*1.0/len(original_message)
    print "false negatives ", false_negatives
    print "false positives ", false_positives

preamble= [1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1]

def start_index(to_decode_file):
    cor1 =  np.correlate(to_decode_file,preamble,"full")
    maximum=max(cor1)
    min_index_of_max=0
    for i in range(0,len(cor1)):
        if  cor1[i]==maximum:
            min_index_of_max= i
    print "value of the mean index is ", min_index_of_max
    return min_index_of_max


def decoding_byte_array(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    print "length of total received array is " , len(to_decode_data), "original length of transmissions", len(oracle_indices)
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        print idx, 
        try :
            d=to_decode_data[idx]
        except:
            print "index is", idx , len(ppm), i
            break
        if (to_decode_data[idx ]==1 and to_decode_data[idx+1]==0 and  to_decode_data[idx+2]==1)  :
            rs_decoder_input.append('0')
            continue
        if (to_decode_data[idx ]==1 and to_decode_data[idx+1] ==1  and to_decode_data[idx+2] ==0) :
            rs_decoder_input.append('1')
            continue
    print len(rs_decoder_input)*1.0/8 , " this must be a number"
    rs_feed=''.join(rs_decoder_input)
    bin_rep_to_decode = bytearray()
    print "length of rs feed is ",len(rs_feed)
    #print "rs feed string is " ,rs_feed
    for i in range(0,len(rs_feed),8):
        x= rs_feed[i:i+8]
        sx=struct.pack('B',int(x,2))
        #print "x: ",x ," ",
        print chr(ord(sx)),
        bin_rep_to_decode.extend(sx)

    return bin_rep_to_decode

def decoding_byte_array2(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    j=0
    import pylab
    pylab.plot(to_decode_data[0:150],'b*-')
    pylab.ylim(0,2)
    pylab.savefig("tocheck.pdf")
    j_last=0
    tup_last=ppm[0]
    print "length of oracle indices/bits to transmit ", len(oracle_indices), "len of to_decode_data",len(to_decode_data)
    print ppm[:10]
    for i in range(0,len(ppm)):
        tup=ppm[i]
        print "(i,j is ",i,j , " tolook= ",tup, ") "
        if tup[1]==101:
            while j < len(to_decode_data):
                if to_decode_data[j] ==1 and to_decode_data[j+1] ==0 and to_decode_data[j+2] ==1 :
                    rs_decoder_input.append('0')
                    print "101 and tup AT j=",j, "j_last-j=",j- j_last, "tup diff= ", tup[0]-tup_last[0]
                    j_last=j
                    j=j+3
                    tup_last=tup
                    break
                else:
                    j=j+1
        if tup[1]==11:
            while j < len(to_decode_data):
                if to_decode_data[j] ==1 and to_decode_data[j+1] ==1 :
                    rs_decoder_input.append('1')
                    print "11 and tup AT j=",j , "j_last=",j-j_last, "tup diff= ", tup[0]-tup_last[0]
                    j_last=j
                    j=j+2
                    tup_last=tup
                    break
                else:
                    j=j+1
     #   if i>20:
     #       sys.exit(1)

    print len(rs_decoder_input)*1.0/8 , " this must be a number"
    rs_feed=''.join(rs_decoder_input)
    bin_rep_to_decode = bytearray()
    print "length of rs feed(string format) is ",len(rs_feed)
    print "length of list created= ", rs_decoder_input
    #print "rs feed string is " ,rs_feed
    for i in range(0,len(rs_feed),8):
        x= rs_feed[i:i+8]
        sx=struct.pack('B',int(x,2))
        #print "x: ",x ," ",
        print chr(ord(sx)),
        bin_rep_to_decode.extend(sx)
    print "\nnow the binary rep list length is= ", len(bin_rep_to_decode)
    return bin_rep_to_decode


def plot_the_instances(to_decode_file,ppm):
    for i in range(0,len(ppm)):
        #d=to_decode_file[idx]
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        plt.plot(to_decode_file[idx: idx+5], "r*-")  
    plt.savefig("start_of_data.pdf")


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
    get_index=start_index(to_decode_file)
    start_data_index = get_index+1 # get_index+1 #(m-get_index)  #m - (len(preamble) - get_index) +1
    print "starting of data is  ", start_data_index
    plt.plot(to_decode_file[:start_data_index],'*-')
    plt.savefig('abhinav.pdf')
    plt.clf()
    plot_the_instances(to_decode_file,oracle_indices)
    original_message =original_string[len(preamble):]
    to_decode_data1= to_decode_file[start_data_index:  ]
    to_decode_data= to_decode_data1.astype(np.int64)
    #print "lengths of data going in:", len(original_message), len(to_decode_data)
    #error_rate_calculations(to_decode_data, original_message)
    bin_rep_to_decode=decoding_byte_array(oracle_indices,to_decode_data)
    #bin_rep_to_decode=decoding_byte_array2(oracle_indices,to_decode_data)
    print "\nGoing to decode"
    rs= reedsolo.RSCodec(32)
    message_decoded = rs.decode(bin_rep_to_decode)
    print "decoded message is ",message_decoded
    print "\n"

if __name__=='__main__':
    main(sys.argv[1:])
