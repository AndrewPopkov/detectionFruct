import cv2
import torch
import numpy as np
import torchvision
from google_drive_downloader import GoogleDriveDownloader as gdd


class Detector():
    def __init__(self):
        gdd.download_file_from_google_drive(file_id='1-9ePvKN0l_QIp_UcIoNrkG0AXOosGuR2',
                                            dest_path='model/rrcnn_0.7881030117472012.pth',
                                            unzip=True)

        use_gpu = torch.cuda.is_available()
        if use_gpu:
            net = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False).cuda()
            net.load_state_dict(torch.load('model/rrcnn_0.7881030117472012.pth'))
            net.eval().cuda()
        else:
            net = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
            net.load_state_dict(torch.load('model/rrcnn_0.7881030117472012.pth'))
            net.eval()


    def plot_preds(numpy_img, preds):
        boxes = preds['boxes'].cpu().detach().numpy()
        if len(boxes) == 0:
            return numpy_img
        for box in boxes:
            numpy_img = cv2.rectangle(
                numpy_img,
                (box[0], box[1]),
                (box[2], box[3]),
                255,
                3
            )
        return numpy_img.get()
    def detect(self, imgPath, targetlabel):
        img_numpy = cv2.imread(imgPath)[:, :, ::-1]
        img = torch.from_numpy(img_numpy.astype('float32')).permute(2, 0, 1)
        img = img / 255.
        if self.use_gpu:
            predictions = self.net(img[None, ...].cuda())
        else:
            predictions = self.net(img[None, ...])
        CONF_THRESH = 0.8
        boxes = predictions[0]['boxes'][(predictions[0]['scores'] > CONF_THRESH) & (predictions[0]['labels'] == targetlabel)]
        boxes_dict = {}
        boxes_dict['boxes'] = boxes
        img_with_boxes = self.plot_preds(img_numpy, boxes_dict)
        cv2.imwrite(imgPath, img_with_boxes)
        return imgPath

