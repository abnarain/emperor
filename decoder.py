import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import numpy as np
import scipy, sys, getopt,struct,reedsolo
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

fig_width = 10
fig_length = 10.25
fig_left = 0.12
fig_right = 0.94
fig_bottom = 0.25
fig_top = 0.94
fig_hspace = 0.5

preamble= [1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1]
def ber_repetition(oracle_indices,to_decode_data):
    ppm= oracle_indices
    print "length of oracle indices/bits to transmit ", len(oracle_indices), "len of to_decode_data",len(to_decode_data)
    print ppm[:10]
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        if tup[1]==111:
            xored_data.append(int(to_decode_data[idx]) ^ int(original_message[idx]))
            if original_message[i] == 1 and  to_decode_data[i] == 0 :
                false_negatives += 1
        elif tup[1] ==000:
            if original_message[i] == 0 and  to_decode_data[i] == 1 :
                false_positives += 1
            xored_data.append(int(to_decode_data[idx]) ^ int(original_message[idx]))
        else:
            print "Impossible !"

    print "False Positives = ", false_positives
    print "False Negatives = ", false_negatives

def ber_single(oracle_indices,to_decode_data, original_message):
    ppm= oracle_indices
    to_decode_data = to_decode_data[:len(original_message)]
    print "\nLast element oracle: ", oracle_indices[-1], "len of to_decode_data ",len(to_decode_data), "messsage size ", len(original_message)
    xored_data=[]
    false_negatives,false_positives =0,0
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        print " idx = ", idx,
        if tup[1]==100:
            xored_data.append(int(to_decode_data[idx]) ^ int(original_message[idx]))
            if original_message[idx] == 1 and  to_decode_data[idx] == 0 :
                false_negatives += 1
        elif tup[1] ==000:
            xored_data.append(int(to_decode_data[idx]) ^ int(original_message[idx]))
            if original_message[idx] == 0 and  to_decode_data[idx] == 1 :
                false_positives += 1
        else:
            print "Impossible!"
    print "False Positives = ", false_positives
    print "False Negatives = ", false_negatives
    print "Bit Error Rate = ", sum(xored_data)*1.0/len(xored_data)

def start_index(to_decode_file):
    cor1 =  np.correlate(to_decode_file,preamble,"full")
    maximum=max(cor1)
    min_index_of_max=0
    for i in range(0,len(cor1)):
        if  cor1[i]==maximum:
            min_index_of_max= i
            break
    print "value of the mean index is ", min_index_of_max
    return min_index_of_max

def decoding_maj2(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    print "length of total received array is " , len(to_decode_data), "original length of transmissions", len(oracle_indices)
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        try :
            d=to_decode_data[idx]
        except:
            print "index is", idx , len(ppm), i
            break
        if ((to_decode_data[idx ]==1 and to_decode_data[idx+1]==1) or (to_decode_data[idx ]==1 and to_decode_data[idx+1]==0)or  (to_decode_data[idx ]==0 and to_decode_data[idx+1]==1 )) :
            rs_decoder_input.append('1')
        elif (to_decode_data[idx ]==0 and to_decode_data[idx+1] ==0 )  :
            rs_decoder_input.append('0') 
        else:
           print "donno"

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


def decoding_maj3(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    print "length of total received array is " , len(to_decode_data), "original length of transmissions", len(oracle_indices)
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        try :
            d=to_decode_data[idx]
        except:
            print "index is", idx , len(ppm), i
            break
        if ((to_decode_data[idx ]==1 and to_decode_data[idx+1]==1 and to_decode_data[idx+2]==1) or (to_decode_data[idx ]==1 and to_decode_data[idx+1]==0 and to_decode_data[idx+2]==1)or  (to_decode_data[idx ]==1 and to_decode_data[idx+1]==1 and to_decode_data[idx+2]==0) or (to_decode_data[idx ]==0 and to_decode_data[idx+1]==1 and to_decode_data[idx+2]==1)  ) :
            rs_decoder_input.append('1')
        elif ((to_decode_data[idx ]==0 and to_decode_data[idx+1] ==0  and to_decode_data[idx+2]==0 ) or (to_decode_data[idx ]==0 and to_decode_data[idx+1]==0 and to_decode_data[idx+2]==1) or (to_decode_data[idx ]==0 and to_decode_data[idx+1]==1 and to_decode_data[idx+2]==0) or (to_decode_data[idx ]==1 and to_decode_data[idx+1]==0 and to_decode_data[idx+2]==0) )  :
            rs_decoder_input.append('0') 
        else:
           print "donno"

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

def single_demod(oracle_indices,to_decode_data):
    ppm= oracle_indices
    rs_decoder_input=[]
    print "\nLength of total received array is " , len(to_decode_data), "original length of transmissions", len(oracle_indices)
    for i in range(0,len(ppm)):
        tup=ppm[i]
        idx=tup[0].astype(np.int64)
        try :
            d=to_decode_data[idx]
        except:
            print "index is", idx , len(ppm), i
            break
        if (to_decode_data[idx ]==1) :
            rs_decoder_input.append('1')
        elif (to_decode_data[idx ]==0): # or to_decode_data[idx+1] ==0 or to_decode_data[idx+2]==0 ) : #or (to_decode_data[idx ]==0 and to_decode_data[idx+1]==0 and to_decode_data[idx+2]==1) )  :
            rs_decoder_input.append('0') 
        else:
           print "donno"
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


def main(argv):
    inputfile=''
    original_file=''
    indices_file=''
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

    print inputfile
    print    inputfile.split('_')

    to_decode_file = scipy.fromfile(open(inputfile), dtype=scipy.float32)
    original_string = scipy.fromfile(open(original_file), dtype=scipy.float32)
    oracle_indices = np.load(indices_file)
    print "\n lengths for measured data:" , len(to_decode_file), "length of orig transmission: ",len(original_string)
    get_index=start_index(to_decode_file)
    start_data_index = get_index+1 # get_index+1 #(m-get_index)  #m - (len(preamble) - get_index) +1
    print "starting of data is  ", start_data_index
    plt.plot(to_decode_file[:start_data_index],'*-')
    plt.savefig('abhinav.pdf')
    plt.clf()
    original_message =original_string[len(preamble):]
    to_decode_data1= to_decode_file[start_data_index:]
    to_decode_data= to_decode_data1.astype(np.int64)
    #print "lengths of data going in:", len(original_message), len(to_decode_data)
    #bin_rep_to_decode=decoding_maj3(oracle_indices,to_decode_data)
    bin_rep_to_decode=single_demod(oracle_indices,to_decode_data)
    ber_single(oracle_indices,to_decode_data, original_message)
    print "\nGoing to decode"
    rs= reedsolo.RSCodec(32)
    message_decoded =''
    try:
        message_decoded = rs.decode(bin_rep_to_decode)
    except:
        print "Cannot decode using RS decoder " 
    print "decoded message is ",message_decoded
    print "\n"

if __name__=='__main__':
    main(sys.argv[1:])
