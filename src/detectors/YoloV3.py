import cv2
import numpy as np 
import argparse
import time
import os
from matplotlib import pyplot as plt

# Made from this tutorial: https://towardsdatascience.com/object-detection-using-yolov3-and-opencv-19ee0792a420

class YOLOv3:
	# Class is responcible for detection with YOLOv3 which has 3 files to interact with
	# labels - A .txt file with a new line for each object that can be detected
	# config - A .config file for training, probably isn't necessary for detection
	# weights - A .weights file trained from darknet
	def __init__(self, model_dir, confidence=0.3):
		self.model_dir = model_dir
		self.confidence = confidence
		self.load_yolo()

	def load_yolo(self):
		# Open files
		for file in os.listdir(self.model_dir):
			file_extension = os.path.splitext(file)[1]
			if file_extension == '.cfg':
				config_path = os.path.join(self.model_dir, file)
			elif file_extension == '.weights':
				weights_path = os.path.join(self.model_dir, file)
			elif file_extension == '.txt':
				classes_path = os.path.join(self.model_dir, file)
		if (file_extension or weights_path or classes_path) is (None):
			print("Data dir is missing files")

		net = cv2.dnn.readNet(weights_path, config_path)
		classes = []
		with open(classes_path, "r") as f:
			classes = [line.strip() for line in f.readlines()]
		self.model = net
		self.classes = classes
		return

	def detect(self, image_path, save_path=None):
		try:
			image, height, width = self.load_image(image_path)
			outputs = self.detect_objects(image, self.model)
			boxes, confs, class_ids = self.get_box_dimensions(outputs, height, width)
			if save_path is not None:
				self.draw_labels(boxes, confs, class_ids, image, save_path)
			return self.format_output(boxes, confs, class_ids, self.classes, image)
		except:
			return None

	def load_image(self, img_path):
		# image loading
		img = cv2.imread(img_path)
		img = cv2.resize(img, None, fx=0.4, fy=0.4)
		height, width, channels = img.shape
		return img, height, width

	def detect_objects(self, img, net):
		blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
		net.setInput(blob)
		outputs = net.forward(net.getUnconnectedOutLayersNames())
		return outputs

	def get_box_dimensions(self, outputs, height, width):
		boxes = []
		confs = []
		class_ids = []
		for output in outputs:
			for detect in output:
				scores = detect[5:]
				class_id = np.argmax(scores)
				conf = scores[class_id]
				if conf > self.confidence:
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

	def draw_labels(self, boxes, confs, class_ids, img, save_path=None):
		colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
		indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
		font = cv2.FONT_HERSHEY_PLAIN
		for i in range(len(boxes)):
			if i in indexes:
				x, y, w, h = boxes[i]
				label = str(self.classes[class_ids[i]])
				color = colors[i]
				print(label)
				print(confs[i])
				cv2.rectangle(img, (x,y), (x+w, y+h), color, thickness=5)
				cv2.putText(img, label, (x, y - 5), font, fontScale=3, color=color, thickness=3)
		# cv2.imshow("Detection", img)
		# cv2.waitKey(0)
		if save_path is not None:
			cv2.imwrite(save_path, img)

	def format_output(self, boxes, confs, class_ids, classes, img):
		'''Convert detection output to the correct format for storing in the geoJSON file'''
		properties = {}
		colors = np.random.uniform(0, 255, size=(len(classes), 3))
		indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
		font = cv2.FONT_HERSHEY_PLAIN
		for i in range(len(boxes)):
			if i in indexes:
				label = str(classes[class_ids[i]])
				print(label)
				try:
					properties[label] += 1
				except KeyError:
					properties[label] = 1
		print(properties)
		return properties