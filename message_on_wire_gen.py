'''
This file generates the message on wire with BPSK modulation into consideration.
Symbol -1, 1 are mapped to bits 1 and 0, while symbol 0 means nothing on the channel.
It lets LO at transmitter transmit nothing.
'''
import reedsolo
import random,binascii, sys,math

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
    corrupted_message = encoded_message[:]
    corrupted_message[2]=101
    corrupted_message[1]=92
    corrupted_message[3]=103
    corrupted_message[5]=104
    corrupted_message[9]=122
    corrupted_message[8]=121
    corrupted_message[17]=119
    corrupted_message[13]=118
    corrupted_message[16]=117
    corrupted_message[13]=116
    corrupted_message[10]=117
    corrupted_message[18]=118
    corrupted_message[19]=119
    corrupted_message[24]=117
    corrupted_message[23]=109
    corrupted_message[22]=110
    corrupted_message[21]=121

    error_bits, tx_instances, tx_indexes=[], [], []
    index, next_instance, error_count=0,0,0

    assert( len(encoded_message) == len(corrupted_message))
    assert len(bit_representation_message)*1.0/len(corrupted_message) ==8.0
    #this is for finding out which bits were flipped in above corruption
    for a,b in zip(encoded_message,corrupted_message):
        error_count += bin(a ^ b).count("1")
        
    print "the total number of bit flips done were ", error_count
    list_1s = list(bit_representation_message)
    sum_of_1s=sum([int(list_1s[i]) for i in range(0,len(list_1s))])
    
    message_length_on_wire= len(bit_representation_message)*len(bit_representation_message)
    print "length of bit representation ", len(bit_representation_message), "message slots on wire(square) ", message_length_on_wire
    tx_indexes.append(0)
    for j in range(0,len(bit_representation_message)-1):
        next_instance=random.uniform(0,message_length_on_wire)
        tx_indexes.append(int(next_instance))
    new_tx= sorted(tx_indexes)

    message_amp_representation=[]
    for i in bit_representation_message:
        if i == '0':
            message_amp_representation.append(1)
        else:
            message_amp_representation.append(-1)

    #import pylab
    #pylab.plot(tx_indexes)
    #pylab.show()
    for i in range(0,message_length_on_wire):
        if i in new_tx:
            tx_instances.append(message_amp_representation[index])
            index = index+1
        else:
            tx_instances.append(0)
        
    import collections
    print "duplicates are ", [item for item, count in collections.Counter(new_tx).items() if count > 1]
    import numpy as np
    a = np.array(tx_instances, dtype=np.float32)
    a.astype('float32').tofile('abh')
    print "len of total tx= " , len(new_tx), " must be = msg len on wire= ", message_length_on_wire
