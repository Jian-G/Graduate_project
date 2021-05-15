from flask import *
import os
import shutil
import logging as rel_log
from datetime import timedelta
from gevent import pywsgi
from gevent import monkey
import glob
from server_udp import  get_info, get_transmitinfo
# from client_udp import client_start
from detect import detect1, get_video_duration
import cv2
import threading
from multiprocessing import cpu_count, Process

monkey.patch_all()
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__, static_folder= "cache/temp", static_url_path="")
app.secret_key = 'secret'

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)


# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config.update(DEBUG=True)

app.config['REDIS_HOST'] = "127.0.0.1" # redis数据库地址
app.config['REDIS_PORT'] = 6379 # redis 端口号


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

@app.route('/')
def index():
    return redirect(url_for('static', filename='./index.html'))

@app.route('/get_frames', methods=['POST'])
def get_frames():
    data = json.loads(request.data)
    filename = "cache/input/" + data['filename']
    frames = cv2.VideoCapture(filename).get(7)
    # print(frames)
    return jsonify({'status': 1,
                        'frames':frames})

@app.route('/detect', methods=['GET','POST'])
def detect():
    data = json.loads(request.data)
    print(data)
    filename = "cache/input/" + data['filename']
    opt = {'weights':'weights/mix_weights.pt','source':filename}
    t_detect = threading.Thread(target=detect1, args=(opt,))
    t_detect.start()
    t_detect.join()
    # detect1(opt)
    return jsonify({'status': 1})

@app.route('/file_list', methods=['GET','POST'])
def get_filelist():
    filename_list = []
    data = request.data
    if data != []:
        data = json.loads(data)
    for filename in data:
        filename_list.append(filename['filename'])
    file_list = []
    for filename in glob.glob(r'cache/temp/*.mp4'):
        if("finish" in filename and filename[11:] not in filename_list):
            file_info = {}
            file_info['filename'] = filename[11:]
            file_info['blocks'], file_info['drops'], file_info['filesize'] = get_info(filename)
            file_info['filesize'] = round(file_info['filesize'] / (1024 * 1024), 2)
            file_list.append(file_info)
    if len(file_list) > 0:
        return jsonify({'status': 1,
                        'file_list':file_list})
    else:
        return jsonify({'status': 0})

@app.route('/detect_result', methods=['GET','POST'])
def get_detectresult():
    filename_list = []
    data = request.data
    if data != []:
        data = json.loads(data)
    for filename in data:
        filename_list.append(filename['filename'])
    detect_result = []
    for filename in glob.glob(r'cache/temp/*.mp4'):
        if("finish" in filename and filename[11:] not in filename_list):
            detect_info = {}
            detect_info['filename'] = filename[11:]
            detect_info['filesize'] = os.path.getsize(filename)
            detect_info['filesize'] = round(detect_info['filesize'] / (1024 * 1024), 2)
            detect_info['time'] = round(get_video_duration(filename),1)
            detect_result.append(detect_info)
    if len(detect_result) > 0:
        return jsonify({'status': 1,
                        'detect_result':detect_result})
    else:
        return jsonify({'status': 0})

@app.route("/transmit_info", methods=['GET','POST'])
def get_transmitinfos():
    transmit_info = get_transmitinfo()
    if len(transmit_info) > 0:
        return jsonify({'status': 1,
                        'transmit_info':transmit_info})
    else:
        return jsonify({'status': 0})
    

server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
server.start()

def serve_forever():
    server.start_accepting()
    server._stop_event.wait()

if __name__ == "__main__":
    # # 服务器发送请求进程
    # server_start()
    # # 多线程响应请求，避免阻塞
    for i in range(3):
        p = Process(target=serve_forever)
        p.start()
        p.join()
    # server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, threaded= True)
    # server.serve_forever()