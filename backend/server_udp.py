#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import math
import argparse
import numpy as np
import FountainCode.core
from FountainCode.encoder import encode
from FountainCode.decoder import decode
from FountainCode import core
from socket import *
import threading
import _thread
import json
import time
import glob
from multiprocessing import cpu_count, Process
import redis,random

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)    # storage send info
r1 = redis.StrictRedis(host="127.0.0.1", port=6379, db=1)   # storage recv info 

def blocks_read(file, filesize):
    """ Read the given file by blocks of `core.PACKET_SIZE` and use np.frombuffer() improvement.

    Byt default, we store each octet into a np.uint8 array space, but it is also possible
    to store up to 8 octets together in a np.uint64 array space.  
    
    This process is not saving memory but it helps reduce dimensionnality, especially for the 
    XOR operation in the encoding. Example:
    * np.frombuffer(b'\x01\x02', dtype=np.uint8) => array([1, 2], dtype=uint8)
    * np.frombuffer(b'\x01\x02', dtype=np.uint16) => array([513], dtype=uint16)
    """
    # core.PACKET_SIZE = getPacketSize(filesize, args.blocks)
    blocks_n = math.ceil(filesize / core.PACKET_SIZE)
    blocks = []

    # Read data by blocks of size core.PACKET_SIZE
    for i in range(blocks_n):
            
        data = bytearray(file.read(core.PACKET_SIZE))

        if not data:
            raise "stop"

        # The last read bytes needs a right padding to be XORed in the future
        if len(data) != core.PACKET_SIZE:
            data = data + bytearray(core.PACKET_SIZE - len(data))
            assert i == blocks_n-1, "Packet #{} has a not handled size of {} bytes".format(i, len(blocks[i]))

        # Paquets are condensed in the right array type
        blocks.append(np.frombuffer(data, dtype=core.NUMPY_TYPE))
    return blocks

def my_encode(filename):
    with open(filename, "rb") as file:
        # print("Redundancy: {}".format(REDUNDANCY))
        # print("Systematic: {}".format(SYSTEMATIC))

        filesize = os.path.getsize(filename)
        # print("Filename: {} ".format(filename))
        # print("Filesize: {} bytes".format(filesize))

        # Splitting the file in blocks & compute drops
        # print("Packet-size: {}".format(PACKET_SIZE))
        file_blocks = blocks_read(file, filesize)
        print(file_blocks[0].dtype)
        file_blocks_n = len(file_blocks)
        drops_quantity = int(file_blocks_n * core.REDUNDANCY)

        print("Blocks: {}".format(file_blocks_n))
        print("Drops: {}\n".format(drops_quantity))
        file_symbols = []

        for curr_symbol in encode(file_blocks, drops_quantity=drops_quantity, filename=filename):
            file_symbols.append(curr_symbol)
        return file_symbols

def get_info(filename):
    with open(filename, "rb") as file:
        filesize = os.path.getsize(filename)
        file_blocks = blocks_read(file, filesize)
        file_blocks_n = len(file_blocks)
        drops_quantity = int(file_blocks_n * core.REDUNDANCY)
        return file_blocks_n,drops_quantity,filesize

def send_file(connection):
    index = 1
    while(True):
        # address = ('10.28.216.46', 8000)
        address = ('127.0.0.1', 8000)
        for filename in glob.glob(r'cache/temp/*.mp4'):
            flag = True
            for fileindex, info in core.FILE_LIST.items():
                if(info['filename'] == filename):
                    flag = False
            if(flag and "finish" in filename):
                value = str({"port":address[1], "host":address[0], "state": -1, 'fileindex':index})
                r.set(name=filename[11:], value= value)
                r1.set(name=filename[11:], value= 'None')
                infos = {'state':-1, 'epoch':0, 'blocks_n':0, 'filename':filename, 'times':0, 'drops': my_encode(filename)}
                core.FILE_LIST[index] = infos
                index += 1
        for fileindex, info in core.FILE_LIST.items():
            if(info['state'] == -1):    # file info packet
                file_blocks_n,drops_quantity,filesize = get_info(core.FILE_LIST[fileindex]['filename'])
                core.FILE_LIST[fileindex]['blocks_n'] = file_blocks_n
                # send the info of file
                packet = core.Packet(packet_type= 1, fileindex= fileindex, blocks= file_blocks_n, drops= drops_quantity, filesize= filesize)
                packet = core.parseArray(packet)
                connection.sendto(packet.tobytes(),address)
                time.sleep(1)
                # print(packet)
            elif(info['state'] == 0):   # data packet
                if(True):
                # if(core.FILE_LIST[filename]['epoch'] == 0):
                    symbols = random.sample(info['drops'], int(len(info['drops'])))
                    for symbol in symbols:
                        symbol = core.parseArray(symbol)
                        symbol[1] = fileindex
                        symbol[7] = core.FILE_LIST[fileindex]['epoch']
                        # print(symbol)
                        # print(sys.getsizeof(symbol.tobytes()))
                        connection.sendto(symbol.tobytes(),address)
                        time.sleep(1/2000.0)
                        # sys.exit()
                    core.FILE_LIST[fileindex]['epoch'] += 1
                # else:
                #     for symbol in info['drops'][info['blocks_n']:]:
                #         # send the data
                #         connection.sendto(symbol.encode('utf-8'), address)
                #         time.sleep(1/1000.0)
            elif(info['state'] == 1 and info['times'] < 3):   # finish ack
                packet = core.Packet(packet_type= 2, fileindex= fileindex)
                packet = core.parseArray(packet)
                connection.sendto(packet.tobytes(),address)
                core.FILE_LIST[fileindex]['times'] += 1
    # connection.close()

def recv_ack(udp_socket):
    while(True):
        recv,address = udp_socket.recvfrom(4096)
        recv = np.frombuffer(recv, dtype=core.NUMPY_TYPE)
        # print(recv)
        packet = core.parsePacket(recv)
        # print(time.time())
        # print(packet.packet_type)
        if (packet.packet_type == 1): # hello packet
            core.CLIENT.append(address)
            print(address)
        elif (packet.packet_type == 2): # ack of file info
            core.FILE_LIST[packet.fileindex]['state'] = 0
            value = str({"port":address[1], "host":address[0], "state": 0,'fileindex':packet.fileindex})
            r.set(name=core.FILE_LIST[packet.fileindex]['filename'][11:], value= value)
        elif(packet.packet_type == 3): # ack of file recovered
            core.FILE_LIST[packet.fileindex]['state'] = 1
            value = str({"port":address[1], "host":address[0], "state": 1,'fileindex':packet.fileindex})
            r.set(name=core.FILE_LIST[packet.fileindex]['filename'][11:], value= value)
            # print(packet.fileindex)

def get_transmitinfo():
    # global file_list, client
    transmit_info = []
    keys = r.keys()
    for filename in keys:
        file_info = {}
        value = eval(r.get(filename))
        # print(value)
        file_info['filename'] = str(filename,encoding="utf-8")
        file_info['port'] = value['port']
        file_info['host'] = value['host']
        # file_info['host']
        if(value['state'] == -1):
            file_info['state'] = "waiting"
        elif(value['state'] == 0):
            file_info['state'] = "transmiting"
        elif(value['state'] == 1):
            file_info['state'] = "finished"
        else:
            file_info['state'] = "error"
        file_info['info'] = str(r1.get(value['fileindex']),encoding='utf-8')
        transmit_info.append(file_info)
    return transmit_info

# def server_start():   
if __name__ == '__main__':
    # file_list = {}
    # client = []
    upd_socket = socket(AF_INET, SOCK_DGRAM)
    address = ('',8001)
    upd_socket.bind(address)
    t_send = threading.Thread(target=send_file, args=(upd_socket,))
    t_recv = threading.Thread(target=recv_ack, args=(upd_socket,))
    t_send.start()
    t_recv.start()
    t_send.join()
    t_recv.join()
