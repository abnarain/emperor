import reedsolo
import random,binascii, sys,math
import collections
import numpy as np

def convert(encoded_message):
    bit_representation_message=''
    for c in encoded_message:
        cc= bin(c)[2:].zfill(8)
        bit_representation_message+=bin(c)[2:].zfill(8)
    print "length of bit representation of encoded message is ", len(bit_representation_message)
    return bit_representation_message

def return_sample_messages():

   #message_to_encode_1 = b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...'

   #message_to_encode_2 = b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...  We need to try out a bigger string to transmit and check how the decoder performs particularly with twice the size of the string that we started in the first try of scewing things up and hope things go well nasty well this time around even with a bigger string.'

    #message_to_encode = b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...  We need to try out a bigger string to transmit and check how the decoder performs particularly with twice the size of the string that we started in the first try of scewing things up and hope things go well nasty well this time around even with a bigger string. This is a slightly bigger and mostly well done text because this will test the things of the RS code, the channel and the scheme in terms of the secrecy as the number of slots to spread the information bits will grow polynomially in terms of number of bits of input. This is also a penultimate vector to deal with unless we do things for even more killer long vector as the final one. There are plenty of experiments to be done right now after this basic step goes in of generating test vectors to transmit and receive over the powerline communication channel.'
    message_to_encode = b'Abhinav Narain is a good person'
    return message_to_encode


def generate_postions(bit_representation_message):
    tx_indexes=[]
    tx_indexes.append(0)
    for j in range(1,len(bit_representation_message)):
        next_instance=random.randint(0,message_length_on_wire)
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
            print "Fucked"
        else:
            None
    print  "newly generated to insert ", len(to_insert)
    print "len of sorted tx indexes= " , len(sorted_tx_indexes)
    print "len of separated_tx= ", len(separated_tx)
    return separated_tx

def ppm_modulation(message_length_on_wire,message_amp_representation, separated_tx):
    preamble=[]
    '''
    for i in range(0,200):
        preamble.extend([1,0,0,1,0,0,1,0,0,1,0,0])
    '''
    preamble= [1,0,1,0,1,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0,0,1,1,1,0,0,0,1,0,1,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1]
        
    tmp_len = max(message_length_on_wire, separated_tx[-1])
    #print separated_tx
    counter,counter_2,counter_3,counter_4  =0,0,0,0
    print "max len is: " ,tmp_len, "last slot", separated_tx[-1]
    new_indexes,tx_instances=[],[]
    j,index=0,0
    for i in range(0,tmp_len):
        #print "starting ", message_amp_representation[index],index
        if i in separated_tx:
            counter +=1
            #print i,
            if message_amp_representation[index]==1:
                new_indexes.append([j,11])
                tx_instances.append(1)
                tx_instances.append(1)
                j=j+2
                counter_3 +=2
                index = index+1
            elif message_amp_representation[index]==0:
                new_indexes.append([j,101])
                tx_instances.append(1)
                tx_instances.append(0)
                tx_instances.append(1)
                j=j+3
                counter_4 +=3
                index = index+1
            else:
                print "This is impossible",message_amp_representation[index]
                sys.exit(1)
        else:
            tx_instances.append(0)
            counter_2 +=1
            j=j+1

    a = np.array(new_indexes, dtype=np.int64)
    #a.astype('int64/float32').tofile('transmission_indexes.dat')
    np.save('transmission_indexes_to_compare_3.dat',a)
    tx_instances=preamble+tx_instances + [0]*1000
    b = np.array(tx_instances, dtype=np.float32)
    b.astype('float32').tofile('preamble_new_transmission_3.dat')
    print "index= " ,index
    np.save('save_preamble_new_transmission_3.dat',b)
    print "tx instances len (final len)= ",len(tx_instances)
    print "times sep tx was found(2040 spots) : ", counter
    print "rest of time spots(416100 -counter= ", counter_2
    print "bit1 added due to #1s ", counter_3
    print "bit1  added due to #0s ",counter_4


if __name__=='__main__':
    rs= reedsolo.RSCodec(32)
    message_to_encode=return_sample_messages()
    encoded_message= rs.encode(message_to_encode)
    print "length of message is ", len(message_to_encode), "length of encoded message is ", len(encoded_message) 

    bit_representation_message=convert(encoded_message)

    error_bits= []
    next_instance, error_count=0,0

    assert len(bit_representation_message)*1.0/len(encoded_message) ==8.0
    #this is for finding out which bits were flipped in above corruption
        
    message_length_on_wire= len(bit_representation_message)*len(bit_representation_message)
    print "length of bit representation ", len(bit_representation_message), "message slots on wire(square) ", message_length_on_wire

    separated_tx=generate_postions(bit_representation_message)

    print "new seperated index ",len(separated_tx)
    print "duplicates are ", [item for item, count in collections.Counter(separated_tx).items() if count > 1]
    message_amp_representation= [int(i) for i in list(bit_representation_message)]
    ppm_modulation(message_length_on_wire,message_amp_representation, separated_tx)
    print " must be = msg len on wire= ", message_length_on_wire


