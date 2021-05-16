# Graduate_project
OCV (Object Detection &amp; LT code &amp; Video Backhaul)

## Backend(Flask)

### Object Detection(Yolov5)

**Content**

* `utils` contains common functions for object detection based on yolo v5.
* `weights` contains model weights (mix_weights.pt, helmet_head_person_l.pt).
* `models` contains core methods of yolo v5.

**Usage** 

```
  python3 detect.py [--weights] [--source] [output] [--img-size] [--conf-thres] [--iou-thres] [--device] 
                 [--view-img] [--save-txt] [ --classes] [--agnostic-nms] [--augment] [--update]
  """
      weights:训练的权重
      source:测试数据，可以是图片/视频路径，也可以是'0'(电脑自带摄像头),也可以是rtsp等视频流
      output:网络预测之后的图片/视频的保存路径
      img-size:网络输入图片大小
      conf-thres:置信度阈值
      iou-thres:做nms的iou阈值
      device:设置设备
      view-img:是否展示预测之后的图片/视频，默认False
      save-txt:是否将预测的框坐标以txt文件形式保存，默认False
      classes:设置只保留某一部分类别，形如0或者0 2 3
      agnostic-nms:进行nms是否也去除不同类别之间的框，默认False
      augment:推理的时候进行多尺度，翻转等操作(TTA)推理
      update:如果为True，则对所有模型进行strip_optimizer操作，去除pt文件中的优化器等信息，默认为False
    """
```
### Founatain Code(LT code)

**Content**
* `core.py` contains the Symbol class, constants and functions that are used in both encoding and decoding.
* `distributions.py` contains the two functions that generate degrees based on the ideal soliton and robust soliton distributions
* `encoder.py` contains the encoding algorithm
* `decoder.py` contains the decoding algorithm

**Usage**
```
$ python3 lt_codes.py filename [-h] [-r REDUNDANCY] [--systematic] [--verbose] [--x86]
```

### Video Backhaul(Socket UDP)

**Content**
* `server_udp.py` contains the server threads: send packet(single), receive ack.(**single transmission**)
* `client_udp.py` contains the client threads: receive packet(single), send ack, recover data.(**single transmission**)
* `servers_udp.py` contains the server threads: send packet(muilt), receive ack.(**muilt transmission**)
* `clients_udp.py` contains the client threads: receive packet(muilt), senc ack, recover data.(**muilt transmission**)

**Usage**
```
$ python3 server_udp.py
$ python3 client_udp.py
or
$ python3 servers_udp.py
$ python3 clients_udp.py
```

### Others

**`app.py`** receive request[GET,POST], send reponse[Display infos]

**Usage**
```
python3 app.py
```

**Cache**
* `input` upload the *.mp4 file,ready for detect
* `temp` save the part of the video after cut, ready for detect
* `receive` save the recovered file


## Frontend(Vue.js)

**Components**
* `Header.vue` Header component, show the title and author
* `Upload.vue` Upload file, detect process bar
* `Table.vue` Show the result of detectation, preview the video
* `Code.vue` Show the result of encoding
* `Transmit.vue` Show the transmission info 
* `Log.vue` Show the operation logs
* `Menu.vue` Left menu for positioning
* `Foot.vue` Footer component, show the copyright

**Usage**
``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```
