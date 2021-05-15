#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *
from FountainCode import core
from FountainCode.decoder import decode
import json
import numpy as np
import struct
import copy
import time,sys
import threading
from multiprocessing import cpu_count, Process
import redis
r = redis.StrictRedis(host="127.0.0.1", port=6379, db=1)

def blocks_write(recovered_blocks, file_copy, filesize):
    """ Write the given blocks into a file
    """
    count = 0
    for data in recovered_blocks[:-1]:
        # print(recovered_blocks)
        file_copy.write(data)
        count += len(data)
    # Convert back the bytearray to bytes and shrink back 
    last_bytes = bytes(recovered_blocks[-1])
    shrinked_data = last_bytes[:filesize % core.PACKET_SIZE]
    file_copy.write(shrinked_data)

def recv_file(connection):
    epoch = 0
    while(True):
        # receive the packet info
        recv,addr = connection.recvfrom(8500)
        # print("{}-{}".format(type(recv),sys.getsizeof(recv)))
        recv = np.frombuffer(recv, dtype=core.NUMPY_TYPE)
        # print(recv)
        packet = core.parsePacket(recv)
        # if(packet.index == 1):
        #     print(packet.data)
        if(packet.packet_type == 1 and packet.fileindex not in core.RECEIVE_LIST.keys()):
            filename, file_blocks_n, drops, filesize = packet.fileindex, packet.blocks, packet.drops, packet.filesize
            info = {'state': 0, 
                    'blocks':[], 
                    'need': file_blocks_n, 
                    'recovered_blocks': [], 
                    'recovered_n': 0,
                    'filesize': filesize,
                    'drops':drops,
                    'indexs':set(),
                    'last_n':file_blocks_n,
                    'start_time':time.time(),
                    'end_time':'',
                    'decode_times':0}
            core.RECEIVE_LIST[filename] = info
        elif(packet.packet_type == 0):
            if core.RECEIVE_LIST[packet.fileindex]['state'] == 0:
                if packet.epoch == 0: # recv first epoch
                    symbol = core.Symbol(index=packet.index,degree=packet.degree,data=packet.data,filename=packet.fileindex)
                    core.RECEIVE_LIST[packet.fileindex]['blocks'].append(symbol)
                    core.RECEIVE_LIST[packet.fileindex]['indexs'].add(packet.index)
                elif packet.epoch != 0 and packet.index not in core.RECEIVE_LIST[packet.fileindex]['indexs']: # recv other epoch
                    symbol = core.Symbol(index=packet.index,degree=packet.degree,data=packet.data,filename=packet.fileindex)
                    core.RECEIVE_LIST[packet.fileindex]['blocks'].append(symbol)
                    core.RECEIVE_LIST[packet.fileindex]['indexs'].add(packet.index)
        elif(packet.packet_type == 2 and packet.fileindex in core.RECEIVE_LIST.keys()):
            value = core.RECEIVE_LIST.pop(packet.fileindex)
        # print(core.RECEIVE_LIST.keys())
        # if(2 in core.RECEIVE_LIST.keys()):
        #     print("length:" + str(len(core.RECEIVE_LIST[2]['blocks'])))
        # print(core.RECEIVE_LIST.keys())
        
def send_ack(udp_socket):
    address = ("127.0.0.1", 8001)
    packet = core.Packet(packet_type= 1)
    packet = core.parseArray(packet)
    udp_socket.sendto(packet.tobytes(),address)
    while(True):
        for fileindex in list(core.RECEIVE_LIST.keys()):
            if(core.RECEIVE_LIST[fileindex]['state'] == 0):
                packet = core.Packet(packet_type= 2, fileindex= fileindex)
                packet = core.parseArray(packet)
                udp_socket.sendto(packet.tobytes(),address)
            elif(core.RECEIVE_LIST[fileindex]['state'] == 1):
                packet = core.Packet(packet_type= 3, fileindex= fileindex)    # success recover the file
                packet = core.parseArray(packet)
                udp_socket.sendto(packet.tobytes(),address)
                print(packet)
        time.sleep(2)

def my_decode():
    while(True):
        for filename in list(core.RECEIVE_LIST.keys()):
            if(filename in core.RECEIVE_LIST.keys() and core.RECEIVE_LIST[filename]['state'] == 0):
                if ((core.RECEIVE_LIST[filename]['last_n'] + int(len(core.RECEIVE_LIST[filename]['blocks']) * 0.01)) < len(core.RECEIVE_LIST[filename]['blocks'])) or (core.RECEIVE_LIST[filename]['drops'] == len(core.RECEIVE_LIST[filename]['blocks'])):
                    temp = copy.deepcopy(core.RECEIVE_LIST[filename]['blocks']) # deep copy
                    core.RECEIVE_LIST[filename]['recovered_blocks'], core.RECEIVE_LIST[filename]['recovered_n'] = decode(temp, blocks_quantity=core.RECEIVE_LIST[filename]['need'])
                    core.RECEIVE_LIST[filename]['last_n'] = len(core.RECEIVE_LIST[filename]['blocks'])
                    temp = None
                    core.RECEIVE_LIST[filename]['decode_times'] += 1

                    # print(filename)
                    # print(core.RECEIVE_LIST[filename]['drops'])
                    # print(len(core.RECEIVE_LIST[filename]['blocks']))
                    # print(core.RECEIVE_LIST[filename]['need'])
                    # print(core.RECEIVE_LIST[filename]['recovered_n'])
                    # print(core.RECEIVE_LIST[filename]['blocks'][1].index)
                    # print(core.RECEIVE_LIST[filename]['blocks'][1].data)
            if filename in core.RECEIVE_LIST.keys() and core.RECEIVE_LIST[filename]['recovered_n'] == core.RECEIVE_LIST[filename]['need'] and core.RECEIVE_LIST[filename]['state'] == 0:
                # new_name = filename.replace('temp','receive')
                # splitted = str(filename).split(".")
                # if len(splitted) > 1:
                #     filename_copy = "".join(splitted[:-1]) + "-copy." + splitted[-1]
                # else:
                #     filename_copy = str(filename) + "-copy"
                # # Write down the recovered blocks in a copy
                filename_copy = "cache/receive/" + str(filename) + ".mp4"
                with open(filename_copy, "wb") as file_copy:
                    blocks_write(core.RECEIVE_LIST[filename]['recovered_blocks'], file_copy, core.RECEIVE_LIST[filename]['filesize'])
                    # print(core.RECEIVE_LIST[filename]['recovered_blocks'][0].dtype)
                    core.RECEIVE_LIST[filename]['state'] = 1
                    core.RECEIVE_LIST[filename]['end_time'] = time.time()
                    print("{} recovered.".format(filename_copy))
                    cost = core.RECEIVE_LIST[filename]['end_time'] - core.RECEIVE_LIST[filename]['start_time']
                    print("Cost {} s".format(cost))
                    print("Decode times: {}".format(core.RECEIVE_LIST[filename]['decode_times']))
                    print("Received: {}, Need:{}".format(len(core.RECEIVE_LIST[filename]['blocks']),core.RECEIVE_LIST[filename]['need']))
            if(filename in core.RECEIVE_LIST.keys() and core.RECEIVE_LIST[filename]['state'] == 0):
                value = str(len(core.RECEIVE_LIST[filename]['blocks'])) + '/' + str(core.RECEIVE_LIST[filename]['need']) + '/' + str(core.RECEIVE_LIST[filename]['drops'])
                r.set(name=str(filename), value= value)
                print("{} \t {}-{}".format(filename, len(core.RECEIVE_LIST[filename]['blocks']), core.RECEIVE_LIST[filename]['need']))
        # time.sleep(2)
# def client_start():
if __name__ == '__main__':

    upd_socket = socket(AF_INET, SOCK_DGRAM)
    address = ('',8000)
    upd_socket.bind(address)

    t_send = threading.Thread(target=recv_file, args=(upd_socket,)) # thread1: send ack
    t_recv = threading.Thread(target=send_ack, args=(upd_socket,)) # thread2: recv packet
    t_decode = threading.Thread(target=my_decode)   # thread3: decode packet
    t_send.start()
    t_recv.start()
    t_decode.start()
    t_recv.join()
    t_send.join()
    t_decode.join()



