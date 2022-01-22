import os

import cv2
import torch
import numpy as np
from PIL import Image
import torchvision
from google_drive_downloader import GoogleDriveDownloader as gdd

class Detector():

    def __init__(self):
        gdd.download_file_from_google_drive(file_id='170wEArJiLdU5lI9Mh-DyNOevoFZs7Y81',
                                            dest_path='model/rrcnn_0.7204322155978944.pth',
                                            unzip=True)

        # use_gpu = torch.cuda.is_available()
        self.use_gpu = False
        if self.use_gpu:
            self.DEVICE = torch.device("cuda")
            self.net = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False,num_classes=4).to(self.DEVICE)
            self.net.load_state_dict(torch.load('model/rrcnn_0.7204322155978944.pth'))
            self.net.eval().to(self.DEVICE)
        else:
            self.DEVICE = torch.device("cpu")
            self.net = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False,num_classes=4).to(self.DEVICE)
            self.net.load_state_dict(torch.load('model/rrcnn_0.7204322155978944.pth', map_location=torch.device('cpu')))
            self.net.eval().to(self.DEVICE)

    def plot_preds(self, numpy_img, preds):
        boxes = preds['boxes'].cpu().detach().numpy()
        if len(boxes) == 0:
            return numpy_img
        for box in boxes:
            numpy_img = cv2.rectangle(numpy_img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), 255, 3)
        return numpy_img

    def detect(self, imgPath, targetlabel):
        img_numpy = cv2.imread(imgPath)
        img = torch.from_numpy(img_numpy[:, :, ::-1].astype('float32')).permute(2, 0, 1)
        img = img / 255.
        if self.use_gpu:
            predictions = self.net(img[None, ...].to(self.DEVICE))
        else:
            predictions = self.net(img[None, ...].to(self.DEVICE))
        CONF_THRESH = 0.8
        boxes = predictions[0]['boxes'][
            (predictions[0]['scores'] > CONF_THRESH) & (predictions[0]['labels'] == targetlabel)]
        boxes_dict = {}
        boxes_dict['boxes'] = boxes
        img_with_boxes = self.plot_preds(img_numpy, boxes_dict)
        newPath=imgPath.replace(os.path.splitext(imgPath)[0], os.path.splitext(imgPath)[0] + '_handled')
        cv2.imwrite(newPath,
                    img_with_boxes)
        return newPath
