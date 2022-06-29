import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from datetime import datetime
from models.experimental import attempt_load, attempt_download
from utils.general import non_max_suppression, set_logging
from utils.torch_utils import select_device

class YOLOv5:
    
    def __init__(self):
        # detection parameters
        self.weights =  './model/last.pt'
        self.imgsz = 640
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.max_det = 1000
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.classes = None
        self.agnostic_nms = False
        self.half = False
        self.hide_conf = True
        self.thickness = 2
        self.rect_thickness = 3
        self.pred_shape = (480, 640, 3)
        self.vis_shape = (800, 600)
        self.color = (0,255,0)

        self.load_model()

    def load_model(self):
        self.model = attempt_load(self.weights, device=self.device)
        self.stride = int(self.model.stride.max())  # model stride
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names  # get class names
        print("YOLO model loaded. Launching on ", self.device)

    def detect(self, frame):
            objs = list() # objects coords.
            out = frame.copy()
            frame = cv2.resize(frame, (self.pred_shape[1], self.pred_shape[0]), interpolation=cv2.INTER_LINEAR)
            frame = np.transpose(frame, (2, 1, 0))

            cudnn.benchmark = True  # set True to speed up constant image size inference

            if self.device.type != 'cpu':
                self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once

            frame = torch.from_numpy(frame).to(self.device)
            frame = frame.float()
            frame /= 255.0
            if frame.ndimension() == 3:
                frame = frame.unsqueeze(0)

            frame = torch.transpose(frame, 2, 3)

            pred = self.model(frame, augment=False)[0]
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)

            # detections per image
            for i, det in enumerate(pred):
                
                img_shape = frame.shape[2:]
                out_shape = out.shape

                s_ = f'{i}: '
                s_ += '%gx%g ' % img_shape  # print string

                if len(det):

                    coords = det[:, :4]

                    gain = min(img_shape[0] / out_shape[0], img_shape[1] / out_shape[1])  # gain  = old / new
                    pad = (img_shape[1] - out_shape[1] * gain) / 2, (
                            img_shape[0] - out_shape[0] * gain) / 2  # wh padding

                    coords[:, [0, 2]] -= pad[0]  # x padding
                    coords[:, [1, 3]] -= pad[1]  # y padding
                    coords[:, :4] /= gain

                    coords[:, 0].clamp_(0, out_shape[1])  # x1
                    coords[:, 1].clamp_(0, out_shape[0])  # y1
                    coords[:, 2].clamp_(0, out_shape[1])  # x2
                    coords[:, 3].clamp_(0, out_shape[0])  # y2

                    det[:, :4] = coords.round()

                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s_ += f"{n} {self.names[int(c)]}{'s' * (n > 1)}, "  # add to string
                        
                    for *xyxy, conf, cls in reversed(det):
                
                        c = int(cls)  # integer class
                        label = self.names[c] if self.hide_conf else f'{self.names[c]} {self.conf:.2f}'

                        tl = self.rect_thickness

                        c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                        cv2.rectangle(out, c1, c2, self.color, thickness=tl, lineType=cv2.LINE_AA)

                        if label:
                            tf = max(tl - 1, 1)  # font thickness
                            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
                            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                            cv2.rectangle(out, c1, c2, self.color, -1, cv2.LINE_AA)  # filled
                            cv2.putText(out, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf,
                                        lineType=cv2.LINE_AA)

                            objs.append((int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])))
                            
            return objs, out

                

