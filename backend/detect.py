import argparse
import time
from pathlib import Path
import sys, os
import datetime
import torch
import torch.backends.cudnn as cudnn
import cv2
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, \
    strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

def detect1(opt,save_img=True):
    # 获取输出文件夹，输入源，权重，参数
    source, weights, view_img, save_txt, imgsz = opt['source'], opt['weights'], None, None, 640
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://'))
    # Directories
    # 创建新文件夹保存结果
    time_stamp = datetime.datetime.now()
    time_stamp = str(time_stamp.strftime('%Y_%m_%d-%H_%M_%S'))
    # save_dir = Path(increment_path(Path('cache/temp') / time_stamp , exist_ok=None))  # increment run
    save_dir = Path('cache/temp', exist_ok=None)
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir


    # Initialize
    set_logging()
    # 获取设备
    device = select_device('cpu')
    # 如果设备为gpu，使用Float16
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    # 加载Float32模型，确保用户设定的输入图片分辨率能整除32(如不能则调整为能整除并返回)
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier 二次分类，默认不使用
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader 通过不同输入源设置不同的数据加载方式
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz)
        # dataset = LoadImages(source, img_size=imgsz)

    else:
        save_img = True
        view_img = True
        dataset = LoadImages(source, img_size=imgsz)
    # Get names and colors 获取类别名字，设置画框颜色
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    t0 = time.time()
    # 进行一次向前推理，测试程序是否正常
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    """
    path 图片/视频路径
    img 进行resize+pad之后的图片
    img0 原size图片
    cap 当读取图片时为None，读取视频时为视频源
    """
    if(source.isdigit()):
        cap = cv2.VideoCapture(int(source))
    count = 0 # number of current frames
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0，归一化处理
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        """
        前向传播 返回pred的shape是(1, num_boxes, 5+num_class)
        h,w为传入网络图片的长和宽，注意dataset在检测时使用了矩形推理，所以这里h不一定等于w
        num_boxes = h/32 * w/32 + h/16 * w/16 + h/8 * w/8
        pred[..., 0:4]为预测框坐标
        预测框坐标为xywh(中心点+宽长)格式
        pred[..., 4]为objectness置信度
        pred[..., 5:-1]为分类结果
        """
        t1 = time_synchronized()
        # print("processing_image:", t1-t0)
        pred = model(img, augment=None)[0]
        t1_ = time_synchronized()
        # print("inference time:", t1_-t1)

        # Apply NMS-非极大值抑制
        """
        pred:前向传播的输出
        conf_thres:置信度阈值
        iou_thres:iou阈值
        classes:是否只保留特定的类别
        agnostic:进行nms是否也去除不同类别之间的框
        经过nms之后，预测框格式：xywh-->xyxy(左上角右下角)
        pred是一个列表list[torch.tensor]，长度为batch_size
        每一个torch.tensor的shape为(num_boxes, 6),内容为box+conf+cls
        """
        pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=None)
        t2 = time_synchronized()

        # Apply Classifier，二次分类，默认不使用
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)
        # Process detections，对每一张照片进行处理
        for i, det in enumerate(pred):  # detections per image
            flag_flame = flag_helmet = True
            # 如果输入源是webcam，则batch_size不为1，取出dataset中的一张图片
            if webcam:  # batch_size >= 1
                p, s, im0 = Path(path[i]), '%g: ' % i, im0s[i].copy()
            else:
                p, s, im0 = Path(path), '', im0s
            # 设置保存图片/视频的路径
            if source.isdigit():
                save_path = str(save_dir / time_stamp ) + '_writing.mp4'
            else:
                filename = source[12:-4]
                save_path = str(save_dir / filename ) + '_writing.mp4'

            # 设置保存框坐标txt文件的路径
            txt_path = str(save_dir / 'labels' / p.stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
            # 设置打印信息，图片长宽
            s += '%gx%g ' % img.shape[2:]  # print string
            # 归一化长宽
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                # 调整预测框坐标，基于原size图片的坐标，坐标格式为xyxy
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results，打印检测到的类别数量
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string
                    if names[int(c)] == 'fire':
                        flag_flame = True
                    if names[int(c)] == 'head':
                        flag_helmet = True

                # Write results，保存预测结果
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        # 将xyxy(左上角+右下角)格式转为xywh(中心点+宽长)格式，并除上w，h做归一化，转化为列表再保存
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')
                    # 在原图上画框
                    if save_img or view_img:  # Add bbox to image
                        label = '%s %.2f' % (names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

            # Print time (inference + NMS)，前向传播+NMS的时间
            print('%sDone. (%.3fs)' % (s, t2 - t1))

            # 展示图片/视频
            # Stream results
            if view_img:
                cv2.imshow(str(p), im0)
                if cv2.waitKey(1) == ord('q'):  # q to quit
                    raise StopIteration
            # 设置保存图片/视频
            # Save results (image with detections)
            # print(flag_flame)
            if save_img:
                if vid_path != save_path:
                    if not source.isdigit():
                        fourcc = 'h264'
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    else:
                        fourcc = 'h264'
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), 10, (1280, 720))
                    vid_path = save_path
                if not source.isdigit():
                    if flag_flame or flag_helmet:
                        vid_writer.write(im0)
                        print("{} saved in {}".format(source, save_path))
                else:
                    if flag_flame or flag_helmet:
                        vid_writer.write(im0)
                        count += 1
                    if count >= 150:
                        vid_writer.release()
                        # 设置保存图片/视频的路径
                        new_path = save_path.replace('writing','finish')
                        os.rename(save_path, new_path)
                        print(new_path + '\thas been saved!')
                        time_stamp = datetime.datetime.now()
                        time_stamp = str(time_stamp.strftime('%Y_%m_%d-%H_%M_%S'))
                        save_path = str(save_dir / time_stamp ) + '.mp4'
                        count = 0
    if not source.isdigit():
        vid_writer.release()
        new_path = save_path.replace('writing','finish')
        os.rename(save_path, new_path)
        print(new_path + '\thas been saved!')
                
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        print(f"Results saved to {save_dir}{s}")
    # 打印总时间
    print('Done. (%.3fs)' % (time.time() - t0))

def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num =cap.get(7)
        duration = frame_num/rate
        return duration
    return -1

if __name__ == '__main__':
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='./mix_weights.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images/somke', help='source') # 1为外界USB摄像头
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='cpu', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='ObjectDetection/runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                detect()
                # 去除pt文件中的优化器等信息
                strip_optimizer(opt.weights)
        else:
            detect()




