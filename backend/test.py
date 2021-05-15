# import server_udp
# import os
# import detect
# import server, client
# opt = {'weights':'weights/mix_weights.pt','source':'cache/input/test22.mov'}


# opt = {'weights':'weights/mix_weights.pt','source':'0'}
# detect.detect1(opt)

# server_udp.server_start()
# import cv2

# # open your target video
# video = cv2.VideoCapture('cache/input/fire.mov')
# print("Loaded video ...")

# # # get size and fps of video
# width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = video.get(cv2.CAP_PROP_FPS)
# fourcc = "h264"

# # create VideoWriter for saving
# outVideo = cv2.VideoWriter('fire1.mp4', cv2.VideoWriter_fourcc(*fourcc), 15, (640, 480))
# print(fps)
# cnt = 0
# while (True):

#     ret, frame = video.read()
#     if not ret:
#         print("... end of video file reached")
#         break

#     # write the frame after processing  
#     outVideo.write(frame)
#     if(cnt > 200):
#         break
#     print(cnt)
#     cnt += 1    
# outVideo.release()

# import numpy as np
# filename
# index = 0
# fileid = 1
# degree = 2
# filesize = np.array([4905811909596523022,1862565468694945200]).astype(np.uint64)
# a = np.array([index, fileid, degree]).astype(np.uint64)
# a = np.append(a,filesize)
# print(type(a))

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
# # plt.rcParams['font.sans-serif']=['STHeiti'] #用来正常显示中文标签

# y1 = np.array([0.05,0.21,0.40,0.65,0.92,1.48])
# y2 = np.array([0.09,0.89,3.07,7.11,16.61,41.0])
# y3 = y1 + y2
# x = np.array([10,30,60,100,150,200])

# plt.plot(x,y1,label='Encoding Time',marker='o',markersize=5)
# plt.plot(x,y2,label='Decoding Time',marker='o',markersize=5)
# plt.plot(x,y3,label='Total Time',marker='o',markersize=5)
# plt.xlabel('File Size(MB)')
# plt.ylabel('Time(s)')
# plt.legend()
# plt.show()

# y1 = np.array([2.32,1.21,0.65,0.36,0.23,0.18])
# y2 = np.array([132.4,31.83,7.11,1.96,0.57,0.26])
# y3 = y1 + y2
# x = np.array([2,4,8,16,32,64])

# plt.plot(x,y1,label='Encoding Time',marker='o',markersize=5)
# plt.plot(x,y2,label='Decoding Time',marker='o',markersize=5)
# plt.plot(x,y3,label='Total Time',marker='o',markersize=5)
# plt.xlabel('Packet Size(KB)',fontsize=12)
# plt.ylabel('Time(s)',fontsize=12)
# plt.legend()
# plt.show()

# y1 = np.array([0.65,0.76,0.99,1.01])
# y2 = np.array([7.11,10.49,13.26,15.11])
# y3 = y1 + y2
# x = np.array([1.2,1.5,1.8,2])

# plt.plot(x,y1,label='Encoding Time',marker='o',markersize=5)
# plt.plot(x,y2,label='Decoding Time',marker='o',markersize=5)
# plt.plot(x,y3,label='Total Time',marker='o',markersize=5)
# plt.xlabel('Redundancy',fontsize=12)
# plt.ylabel('Time(s)',fontsize=12)
# plt.legend()
# plt.show()

# y1 = np.array([3.32,10.69,18.10,22.76,39.09,63.83])
# y2 = np.array([3.12,8.93,14.56,20.20,35.52,60.08])
# y3 = np.array([2.86,7.08,12,19.15,33.64,58.29])
# y4 = np.array([2.85,6.17,10.79,17.39,31.65,57.26])
# y5 = np.array([2.82,5.70,10.03,16.93,30.03,56.15])
# x = np.array([10,40,60,100,150,200])

# plt.plot(x,y1,label='One Thread',marker='o',markersize=5)
# plt.plot(x,y2,label='Two Threads',marker='o',markersize=5)
# plt.plot(x,y3,label='Three Threads',marker='o',markersize=5)
# plt.plot(x,y4,label='Four Threads',marker='o',markersize=5)
# plt.plot(x,y5,label='Five Threads',marker='o',markersize=5)

# plt.xlabel('File Size(MB)')
# plt.ylabel('Time(s)')
# plt.legend()
# plt.show()

# y1 = np.array([2,2.6,2.3,2.6,2.6,3.3])
# y2 = np.array([3,2.6,3.3,3.6,4,3.6])
# y3 = np.array([2,2,2.6,3.6,3.6,4])
# y4 = np.array([2,2.6,2.6,3,4,4])
# y5 = np.array([2,2.6,2.3,2.3,3.3,3.3])
# x = np.array([10,40,60,100,150,200])

# plt.plot(x,y1,label='One Thread',marker='o',markersize=5)
# plt.plot(x,y2,label='Two Threads',marker='o',markersize=5)
# plt.plot(x,y3,label='Three Threads',marker='o',markersize=5)
# plt.plot(x,y4,label='Four Threads',marker='o',markersize=5)
# plt.plot(x,y5,label='Five Threads',marker='o',markersize=5)

# plt.xlabel('File Size(MB)')
# plt.ylabel('Decode Times')
# plt.legend()
# plt.show()

y1 = np.array([0.1,0.14,0.17,0.14,0.10,0.10])
y2 = np.array([0.1,0.11,0.13,0.13,0.10,0.07])
y3 = np.array([0.11,0.10,0.13,0.11,0.07,0.06])
y4 = np.array([0.13,0.11,0.14,0.10,0.09,0.06])
y5 = np.array([0.13,0.10,0.13,0.13,0.10,0.08])
x = np.array([10,40,60,100,150,200])

plt.plot(x,y1,label='One Thread',marker='o',markersize=5)
plt.plot(x,y2,label='Two Threads',marker='o',markersize=5)
plt.plot(x,y3,label='Three Threads',marker='o',markersize=5)
plt.plot(x,y4,label='Four Threads',marker='o',markersize=5)
plt.plot(x,y5,label='Five Threads',marker='o',markersize=5)

plt.xlabel('File Size(MB)')
plt.ylabel('Redundancy')
plt.legend()
plt.show()