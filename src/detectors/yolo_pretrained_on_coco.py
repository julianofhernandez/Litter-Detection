import cv2
import numpy as np 
import argparse
import time
from matplotlib import pyplot as plt

# Made from this tutorial: https://towardsdatascience.com/object-detection-using-yolov3-and-opencv-19ee0792a420


class YoloPretrainedOnCoco:
	def load_yolo(self):
		net = cv2.dnn.readNet("models/yolov3-pretrained-coco.weights", "models/yolov3-pretrained-coco.cfg")
		classes = []
		with open("models/coco-labels.txt", "r") as f:
			classes = [line.strip() for line in f.readlines()]
		layers_names = net.getLayerNames()
		output_layers = net.getUnconnectedOutLayersNames()  
		colors = np.random.uniform(0, 255, size=(len(classes), 3))
		return net, classes, colors, output_layers

	def load_image(self, img_path):
		# image loading
		img = cv2.imread(img_path)
		img = cv2.resize(img, None, fx=0.4, fy=0.4)
		height, width, channels = img.shape
		return img, height, width, channels

	def detect_objects(self, img, net, outputLayers):			
		blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
		net.setInput(blob)
		outputs = net.forward(outputLayers)
		return blob, outputs

	def get_box_dimensions(self, outputs, height, width):
		boxes = []
		confs = []
		class_ids = []
		for output in outputs:
			for detect in output:
				scores = detect[5:]
				class_id = np.argmax(scores)
				conf = scores[class_id]
				if conf > 0.3:
					center_x = int(detect[0] * width)
					center_y = int(detect[1] * height)
					w = int(detect[2] * width)
					h = int(detect[3] * height)
					x = int(center_x - w/2)
					y = int(center_y - h / 2)
					boxes.append([x, y, w, h])
					confs.append(float(conf))
					class_ids.append(class_id)
		return boxes, confs, class_ids

	def draw_labels(self, boxes, confs, colors, class_ids, classes, img): 
		indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
		font = cv2.FONT_HERSHEY_PLAIN
		for i in range(len(boxes)):
			if i in indexes:
				x, y, w, h = boxes[i]
				label = str(classes[class_ids[i]])
				color = colors[i]
				cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
				cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
		cv2.imshow("Image", img)

	def image_detect(self, img_path): 
		model, classes, colors, output_layers = self.load_yolo()
		image, height, width, channels = self.load_image(img_path)
		blob, outputs = self.detect_objects(image, model, output_layers)
		boxes, confs, class_ids = self.get_box_dimensions(outputs, height, width)
		self.draw_labels(boxes, confs, colors, class_ids, classes, image)
		while True:
			key = cv2.waitKey(1)
			if key == 27:
				break
