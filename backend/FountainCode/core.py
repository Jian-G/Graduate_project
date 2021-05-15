import os
import sys
import math
import time
import numpy as np
import random
from random import choices
import json

REDUNDANCY = 1.2
SYSTEMATIC = False
VERBOSE = False

# PACKET_SIZE = 524288 * 8
# PACKET_SIZE = 65536
# PACKET_SIZE = 32768
# PACKET_SIZE = 16384
PACKET_SIZE = 8192
# PACKET_SIZE = 4096
# PACKET_SIZE = 2048
# PACKET_SIZE = 1024
# PACKET_SIZE = 512
# PACKET_SIZE = 128
ROBUST_FAILURE_PROBABILITY = 0.01
NUMPY_TYPE = np.uint64
# NUMPY_TYPE = np.uint32
# NUMPY_TYPE = np.uint16
# NUMPY_TYPE = np.uint8
EPSILON = 0.0001
FILE_LIST = {}
CLIENT = []
INDEX = 0
SERVERS = 3
RECEIVE_LIST = {}
class Symbol:
    __slots__ = ["index", "degree", "data", "neighbors","filename"] # fixing attributes may reduce memory usage

    def __init__(self, index, degree, data, filename):
        self.filename = filename
        self.index = index
        self.degree = degree
        self.data = data

    def log(self, blocks_quantity):
        neighbors, _ = generate_indexes(self.index, self.degree, blocks_quantity)
        print("symbol_{} degree={}\t {}".format(self.index, self.degree, neighbors))


class Packet:
    __slots__ = ["packet_type","fileindex","index", "degree", "data", "filesize","blocks", "drops", "epoch"] # fixing attributes may reduce memory usage

    def __init__(self, packet_type= 0, fileindex= 0, index=0, degree=0, data=0, filesize=0, blocks=0, drops=0, epoch=0):
        self.packet_type = packet_type
        self.fileindex = fileindex
        self.index = index
        self.degree = degree
        self.filesize = filesize
        self.blocks = blocks
        self.drops = drops
        self.data = data
        self.epoch = epoch

def parseArray(packet):
    head = np.array([packet.packet_type, packet.fileindex, packet.index, packet.degree, packet.filesize, packet.blocks, packet.drops, packet.epoch]).astype(NUMPY_TYPE)
    data = np.array(packet.data).astype(NUMPY_TYPE)
    whole = np.append(head, packet.data).astype(NUMPY_TYPE)
    return whole

def parsePacket(array):
    packet = Packet(
            packet_type=int(array[0]), 
            fileindex=int(array[1]), 
            index=int(array[2]), 
            degree=int(array[3]), 
            filesize=int(array[4]),
            blocks=int(array[5]), 
            drops=int(array[6]), 
            epoch=int(array[7]),
            data=array[8:].astype(NUMPY_TYPE))
    return packet
    

def parseSymbol(symbol):
    return json.dumps({
        'filename':symbol.filename,
        'index':symbol.index,
        'degree':symbol.degree,
        'data':symbol.data.tolist()})


'''
    t:packet_type
    n:filename
    i:index
    g:degree
    d:data
    z:filesize
    p:drops
    b:blocks
    e:epoch
'''
def parseJson(packet):
    data = {'t':packet.packet_type,
        'n':packet.filename,
        'i':packet.index,
        'g':packet.degree,
        'd':packet.data,
        's':packet.filesize,
        'p':packet.drops,
        'b':packet.blocks,
        'e':packet.epoch}
    return json.dumps(data)

def generate_indexes(symbol_index, degree, blocks_quantity):
    """Randomly get `degree` indexes, given the symbol index as a seed

    Generating with a seed allows saving only the seed (and the amount of degrees) 
    and not the whole array of indexes. That saves memory, but also bandwidth when paquets are sent.

    The random indexes need to be unique because the decoding process uses dictionnaries for performance enhancements.
    Additionnally, even if XORing one block with itself among with other is not a problem for the algorithm, 
    it is better to avoid uneffective operations like that.

    To be sure to get the same random indexes, we need to pass 
    """
    if SYSTEMATIC and symbol_index < blocks_quantity:
        indexes = [symbol_index]               
        degree = 1     
    else:
        random.seed(symbol_index)
        indexes = random.sample(range(blocks_quantity), degree)
    # print(indexes)
    # print(degree)
    return indexes, degree

def log(process, iteration, total, start_time):
    """Log the processing in a gentle way, each seconds"""
    global log_actual_time
    
    if "log_actual_time" not in globals():
        log_actual_time = time.time()

    if time.time() - log_actual_time > 1 or iteration == total - 1:
        
        log_actual_time = time.time()
        elapsed = log_actual_time - start_time + EPSILON
        speed = (iteration + 1) / elapsed * PACKET_SIZE / (1024 * 1024)

        print("-- {}: {}/{} - {:.2%} symbols at {:.2f} MB/s       ~{:.2f}s".format(
            process, iteration + 1, total, (iteration + 1) / total, speed, elapsed), end="\r", flush=True)