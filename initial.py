#!/usr/bin/env python3

# SYSTEM STATE
target_model = []
energy = 0
high_harmoncs = False
bot_count = 1
time_step = 0

nanobot_states =  []
nanobot_states.append ((0, (0,0,0), [1,19] ) )  #  (bid, position, available seeds)


def is_filled(x,y,z,resolution):
    return target_model[ (x * resolution * resolution + y * resolution + z  ) ]

def count_filled(resolution):
    counter = 0
    for x in range(resolution):
        for y in range(resolution):
            for z in range(resolution):
                if(is_filled(x,y,z,resolution)):
                    counter = counter + 1
    print(counter)
    return(counter)

def  count_floor(floor, resolution ):
    counter = 0
    for x in range(resolution):
        for z in range(resolution):
            if (is_filled(x,floor,z,resolution) ):
                counter = counter + 1
                # print("dum dum dum ")
    # print("hi")
    return counter

def count_floor_sanity_check(resolution):
    for i in range(R):
        print(i)
        print(count_floor(i, R))
        new_count = new_count + count_floor(i,R)
    print(new_count)


with open("LA001_tgt.mdl", "rb") as f:
    byte = f.read(1)
    i = 0
    R = int.from_bytes( byte, byteorder = 'little' )
    print("resolution is: " )
    print( R )
    # print(int.from_bytes( resolution, byteorder = 'big' ) )

    while (byte):
        i = i + 1
        # if ( byte[0] & (0b00000100) ):
            # print("BINGO")
        target_model.append( byte[0] & (0b00000001) )
        target_model.append( byte[0] & (0b00000010) )
        target_model.append( byte[0] & (0b00000100) )
        target_model.append( byte[0] & (0b00001000) )
        target_model.append( byte[0] & (0b00010000) )
        target_model.append( byte[0] & (0b00100000) )
        target_model.append( byte[0] & (0b01000000) )
        target_model.append( byte[0] & (0b10000000) )
        byte = f.read(1)
        # print (int.from_bytes(byte,byteorder = 'big'))
print("bytes read:")
print(i)
print("filled pixels:")
print(count_filled(R))
new_count = 0
