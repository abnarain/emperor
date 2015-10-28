import reedsolo
import random,binascii, sys,math
import collections
import numpy as np
if __name__=='__main__':
    rs= reedsolo.RSCodec(32)
    message_to_encode = b'I am going to use RS Encoder. There is basically so much to do that I cannot believe. We need to do as much we can how much we can and keep doing it unless we get success in it and that is how the world works. Lets do it...'
    encoded_message= rs.encode(message_to_encode)
    print "length of message is ", len(message_to_encode), "length of encoded message is ", len(encoded_message) 
    #encoded_string_bytes_1= rs.encode('hello world motherfucker')
    #print encoded_string_bytes, binascii.hexlify(encoded_string_bytes), type(encoded_string_bytes)
    bit_representation_message=''
    justbits_1 =''
    for c in encoded_message:
        cc= bin(c)[2:].zfill(8)
        #print "value of c is", c, int(c), "removing 0b is", bin(c)[2:] , hex((c)), type(c), type(cc)
        #print "value of cc in bin zfill",len(cc), cc, type(cc) ,int(cc), hex(int(cc,2))
        justbits_1+=bin(c)[2:]
        bit_representation_message+=bin(c)[2:].zfill(8)
    print "length of bit representation of encoded message is ", len(bit_representation_message)
    error_bits, tx_instances, tx_indexes=[], [], []
    index, next_instance, error_count=0,0,0

    assert len(bit_representation_message)*1.0/len(encoded_message) ==8.0
    #this is for finding out which bits were flipped in above corruption
        
    message_length_on_wire= len(bit_representation_message)*len(bit_representation_message)
    print "length of bit representation ", len(bit_representation_message), "message slots on wire(square) ", message_length_on_wire
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





    print "new seperated index ",len(separated_tx), "early sorted list length ",len(sorted_tx_indexes), "newly generated to insert ", len(to_insert)
    print "duplicates are ", [item for item, count in collections.Counter(separated_tx).items() if count > 1]
    counter,counter_2,counter_3,counter_4  =0,0,0,0
    message_amp_representation= [int(i) for i in list(bit_representation_message)]
    tmp_len = max(message_length_on_wire, separated_tx[-1])
    #print separated_tx
    print "max len is: " ,tmp_len, separated_tx[-1]
    for i in range(0,tmp_len):
        #print "starting ", message_amp_representation[index],index
        if i in separated_tx:
            counter +=1
            #print i,
            if message_amp_representation[index]==1:
                tx_instances.append(1)
                tx_instances.append(1)
                counter_3 +=2
                index = index+1
            elif message_amp_representation[index]==0:
                tx_instances.append(1)
                tx_instances.append(0)
                tx_instances.append(1)
                counter_4 +=3
                index = index+1
            else:
                print "This is impossible",message_amp_representation[index]
                sys.exit(1)
        else:
            tx_instances.append(0)
            counter_2 +=1

    preamble=[]
    for i in range(0,10):
        preamble.extend([1,0,0,1,1,1,0,0,0,1])
    #print preamble
    
    tx_instances=preamble+tx_instances
    print tx_instances[0:70]
    #import pylab
    #pylab.plot(tx_instances)
    #pylab.show()
    a = np.array(tx_instances, dtype=np.float32)
    a.astype('float32').tofile('preamble_new_transmission.dat')
    print "index= " ,index
    print "len of sorted tx indexes= " , len(sorted_tx_indexes)
    print "len of separated_tx= ", len(separated_tx)
    print " must be = msg len on wire= ", message_length_on_wire
    print "tx instances len (final len)= ",len(tx_instances)
    print "times sep tx was found(2040 spots) : ", counter
    print "rest of time spots(416100 -counter= ", counter_2
    print "bit1 added due to #1s ", counter_3
    print "bit1  added due to #0s ",counter_4

