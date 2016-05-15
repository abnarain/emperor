import reedsolo
import random,binascii, sys,math
import collections
import numpy as np

orig_preamble= [1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1]
preamble48=[1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,1,0,1,0,0,0,1,1]
preamble=[1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,1,1,1,0,1,0,1]

def convert(encoded_message):
    bit_rep_of_msg=''
    for c in encoded_message:
        cc= bin(c)[2:].zfill(8)
        bit_rep_of_msg+=bin(c)[2:].zfill(8)
    print "length of bit representation of encoded message is ", len(bit_rep_of_msg)
    return bit_rep_of_msg

def return_sample_messages(option):
    if option ==1:
        return b'Abhinav Narain is good'
    elif option ==2:
        return b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...'
    elif option ==3: #400
        return b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...  We need to try out a bigger string to transmit and check how the decoder performs particularly with twice the size of the string that we started in the first trial or not'
    elif option ==4: #800
        return b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it... We need to try out a bigger string to transmit and check how the decoder performs particularly with twice the size of the string that we started in the first try of scewing things up and hope things go well nasty well this time around even with a bigger string. This is a slightly bigger and mostly well done text because this will test the things of the RS code, the channel and the scheme in terms of the secrecy as the number of slots to spread the information bits will grow polynomially in terms of number of bits of input. This is also a penultimate vector to deal with.' 
    elif option ==5:
        return b'This is a good opportunitity to try to get transmission'    
    elif option ==6: #80 bytes
        return b'This is a good opportunity to try to do transmission, Master. Sith rule forever.'
    elif option ==7: #25 bytes
        return b'This is good opportunity.'
    elif option ==8: #40
        return b'This is good opportunity. We have to do something!'        
    else:
        print "giving correct input"
        sys.exit(1)



def generate_positions(bit_rep_of_msg,msg_len_on_wire):
    tx_indexes=[]
    tx_indexes.append(0)
    for j in range(1,len(bit_rep_of_msg)):
        next_instance=random.randint(0,msg_len_on_wire)
        tx_indexes.append(int(next_instance))
    sorted_tx_indexes= sorted(tx_indexes)
    separated_tx=[]
    sep_length=0
    to_insert=[]
    for i in range(0,len(sorted_tx_indexes)):
        if  sorted_tx_indexes[i] -sorted_tx_indexes[i-1] >3:
            separated_tx.append(sorted_tx_indexes[i-1])
            sep_length +=1
        else:
            to_insert.append(random.randint(sorted_tx_indexes[i],sorted_tx_indexes[i+1]+4))

    s1 = separated_tx +to_insert
    separated_tx=sorted(s1)
    for i in range(1,len(separated_tx)):
        if  separated_tx[i] -separated_tx[i-1] <3:
            print "Still indexes not far enough. Try again!"
            sys.exit(1)
        else:
            None
    print  "newly generated to insert ", len(to_insert)
    print "len of sorted tx indexes= " , len(sorted_tx_indexes)
    print "len of separated_tx= ", len(separated_tx)
    return separated_tx

def singlepulse_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name):
    tmp_len = max(msg_len_on_wire, separated_tx[-1])
    #print separated_tx
    counter,counter_2,counter_3,counter_4  =0,0,0,0
    print "max len is: " ,tmp_len, "last slot", separated_tx[-1]
    new_indexes,tx_instances=[],[]
    j,index=0,0
    for i in range(0,tmp_len):
        #print "starting ", msg_amp_rep[index],index
        if i in separated_tx:
            counter +=1
            #print i,
            if msg_amp_rep[index]==1:
                new_indexes.append([j,100])
                tx_instances.append(1)
                tx_instances.append(0)
                tx_instances.append(0)
                j=j+3
                counter_3 +=3
                index = index+1
            elif msg_amp_rep[index]==0:
                new_indexes.append([j,000])
                tx_instances.append(0)
                tx_instances.append(0)
                tx_instances.append(0)
                j=j+3
                counter_4 +=3
                index = index+1
            else:
                print "This is impossible",msg_amp_rep[index]
                sys.exit(1)
        else:
            tx_instances.append(0)
            counter_2 +=1
            j=j+1

    a = np.array(new_indexes, dtype=np.int64)
    #a.astype('int64/float32').tofile('transmission_indexes.dat')
    np.save(file_name+'_tx_indexes.dat',a)
    tx_instances=preamble+tx_instances + [0]*10000+[1]

    b = np.array(tx_instances, dtype=np.float32)
    b.astype('float32').tofile(file_name+'_new_tx.dat')
    np.save(file_name+'_save_new_tx.dat',b)

    print "tx instances len (final len)= ",len(tx_instances), "index= ",index
    print "times sep tx was found (length of loop) : ", counter
    print "rest of time spots",tmp_len ," - ",counter, "= ", counter_2
    print "bit1 added due to #1s ", counter_3
    print "bit1  added due to #0s ",counter_4


def am_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name):
    tmp_len = max(msg_len_on_wire, separated_tx[-1])
    #print separated_tx
    counter,counter_2,counter_3,counter_4  =0,0,0,0
    print "max len is: " ,tmp_len, "last slot", separated_tx[-1]
    new_indexes,tx_instances=[],[]
    j,index=0,0
    for i in range(0,tmp_len):
        #print "starting ", msg_amp_rep[index],index
        if i in separated_tx:
            counter +=1
            #print i,
            if msg_amp_rep[index]==1:
                new_indexes.append([j,110])
                tx_instances.append(1)
                tx_instances.append(1)
                tx_instances.append(0)
                j=j+3
                counter_3 +=3
                index = index+1
            elif msg_amp_rep[index]==0:
                new_indexes.append([j,000])
                tx_instances.append(0)
                tx_instances.append(0)
                tx_instances.append(0)
                j=j+3
                counter_4 +=3
                index = index+1
            else:
                print "This is impossible",msg_amp_rep[index]
                sys.exit(1)
        else:
            tx_instances.append(0)
            counter_2 +=1
            j=j+1

    a = np.array(new_indexes, dtype=np.int64)
    #a.astype('int64/float32').tofile('transmission_indexes.dat')
    np.save(file_name+'_tx_indexes.dat',a)
    tx_instances=preamble+tx_instances + [0]*10000+[1]

    b = np.array(tx_instances, dtype=np.float32)
    b.astype('float32').tofile(file_name+'_new_tx.dat')
    np.save(file_name+'_save_new_tx.dat',b)
    print "tx instances len (final len)= ",len(tx_instances), "index= ",index
    print "times sep tx was found (length of loop) : ", counter
    print "rest of time spots",tmp_len ," - ",counter, "= ", counter_2
    print "bit1 added due to #1s ", counter_3
    print "bit1  added due to #0s ",counter_4


def ppm_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name):
    tmp_len = max(msg_len_on_wire, separated_tx[-1])
    #print separated_tx
    counter,counter_2,counter_3,counter_4  =0,0,0,0
    print "max len is: " ,tmp_len, "last slot", separated_tx[-1]
    new_indexes,tx_instances=[],[]
    j,index=0,0
    for i in range(0,tmp_len):
        #print "starting ", msg_amp_rep[index],index
        if i in separated_tx:
            counter +=1
            #print i,
            if msg_amp_rep[index]==1:
                new_indexes.append([j,111])
                tx_instances.append(1)
                tx_instances.append(1)
                tx_instances.append(1)
                j=j+3
                counter_3 +=3
                index = index+1
            elif msg_amp_rep[index]==0:
                new_indexes.append([j,000])
                tx_instances.append(0)
                tx_instances.append(0)
                tx_instances.append(0)
                j=j+3
                counter_4 +=3
                index = index+1
            else:
                print "This is impossible",msg_amp_rep[index]
                sys.exit(1)
        else:
            tx_instances.append(0)
            counter_2 +=1
            j=j+1

    a = np.array(new_indexes, dtype=np.int64)
    #a.astype('int64/float32').tofile('transmission_indexes.dat')
    np.save(file_name+'_tx_indexes.dat',a)
    tx_instances=preamble+tx_instances + [0]*10000+[1]

    b = np.array(tx_instances, dtype=np.float32)
    b.astype('float32').tofile(file_name+'_new_tx.dat')
    print "index= " ,index
    np.save(file_name+'_save_new_tx.dat',b)

    print "tx instances len (final len)= ",len(tx_instances)
    print "times sep tx was found (length of loop) : ", counter
    print "rest of time spots",tmp_len ," - ",counter, "= ", counter_2
    print "bit1 added due to #1s ", counter_3
    print "bit1  added due to #0s ",counter_4


def v1_message_creation(message_option):
    '''
    Uses the O() constant as 1
    The only option used is 6 (as it is largest the sync can handle.)
    '''
    message_to_encode=return_sample_messages(int(message_option))
    encoded_message= rs.encode(message_to_encode)
    print "length of message is ", len(message_to_encode)
    print "length of encoded message is ", len(encoded_message) 
    bit_rep_of_msg=convert(encoded_message)
    assert len(bit_rep_of_msg)*1.0/len(encoded_message) ==8.0
    #this is for finding out which bits were flipped in above corruption
    msg_len_on_wire= len(bit_rep_of_msg)*len(bit_rep_of_msg)
    print "length of bit representation ", len(bit_rep_of_msg), "message slots on wire(square) ", msg_len_on_wire
    separated_tx=generate_positions(bit_rep_of_msg,msg_len_on_wire)
    return [msg_len_on_wire,separated_tx, bit_rep_of_msg]

def v2_message_creation(message_option):
    '''
    This version will increase the constant in front of O() notation to cram
    more bits to look at the resulting covertness offered.
    '''
    message_to_encode=return_sample_messages(int(message_option))
    encoded_message=rs.encode(message_to_encode)
    bit_rep_of_msg=convert(encoded_message)
    assert len(bit_rep_of_msg)*1.0/len(encoded_message) ==8.0
    msg_len_on_wire = ((80+32)*8)**2
    separated_tx=generate_positions(bit_rep_of_msg, msg_len_on_wire)
    return [msg_len_on_wire, separated_tx, bit_rep_of_msg]

if __name__=='__main__':
    if len(sys.argv) <2:
        print "Usage: message_..py <fileName> <messageOption> <BitRepetition> \n"
        sys.exit(1)
    file_name=sys.argv[1]
    rs=reedsolo.RSCodec(32)
    message_option = '1'
    bit_repetition ='3'
    message_option=sys.argv[2]
    bit_repetition=sys.argv[3]

    rep= int(bit_repetition)
    file_name=file_name+'_v'+message_option+'_'+bit_repetition

    #[msg_len_on_wire,separated_tx,bit_rep_of_msg] =v1_message_creation(message_option)

    [msg_len_on_wire,separated_tx,bit_rep_of_msg] = v2_message_creation(message_option)

    print "new seperated index ",len(separated_tx)
    print "duplicates are ", [item for item, count in collections.Counter(separated_tx).items() if count > 1]
    msg_amp_rep= [int(i) for i in list(bit_rep_of_msg)]
    
    #the function names are incorrect. They are all doing repetition coding of the single bit essentially
    if rep==3:
        ppm_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name)
    elif rep==2:
        am_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name)
    elif rep==1:
        singlepulse_modulation(msg_len_on_wire,msg_amp_rep, separated_tx,file_name)
    else:
        print "fix the Coding scheme"
