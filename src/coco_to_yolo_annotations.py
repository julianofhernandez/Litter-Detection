import cv2
from tqdm import tqdm
import os
from shutil import copyfile
import json
import argparse

def get_img_shape(path):
    try:
        img = cv2.imread(path)
        return img.shape
    except AttributeError:
        print('error! ', path)
        return (None, None, None)

def convert_labels(path, x1, y1, x2, y2):
    '''
    Definition: Parses label files to extract label and bounding box
    coordinates. Converts (x1, y1, x1, y2) KITTI format to
    (x, y, width, height) normalized YOLO format.
    '''
    def sorting(l1, l2):
        if l1 > l2:
            lmax, lmin = l1, l2
            return lmax, lmin
        else:
            lmax, lmin = l2, l1
            return lmax, lmin
    size = get_img_shape(path)
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1./size[1]
    dh = 1./size[0]
    x = (xmin + xmax)/2.0
    y = (ymin + ymax)/2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

annotations_file = 'annotations.json'
output_folder = 'yolo_format'

f = open(annotations_file)
training_data = json.load(f)
try:
    os.mkdir(output_folder)
    os.mkdir(os.path.join(output_folder, 'images'))
    os.mkdir(os.path.join(output_folder, 'labels'))
except:
    pass

for i in tqdm(range(len(training_data['categories']))):
    file = open(os.path.join(output_folder, 'classes.txt'), 'a+')
    file.write(str(training_data['categories'][i]['name']))
    file.write('\n')
    file.close()

check_set = set()
for i in tqdm(range(len(training_data['annotations']))):
    image_id = int(training_data['annotations'][i]['image_id'])
    category_id = str(training_data['annotations'][i]['category_id'])
    bbox = training_data['annotations'][i]['bbox']
    image_path = training_data['images'][image_id]['file_name']
    kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
    yolo_bbox = convert_labels(image_path, kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])
    filename = os.path.join(output_folder, 'labels', str(image_id) + '.txt')
    content = category_id + ' ' + str(yolo_bbox[0]) + ' ' + str(yolo_bbox[1]) + ' ' + str(yolo_bbox[2]) + ' ' + str(yolo_bbox[3])
    copyfile(image_path, os.path.join(output_folder, 'images', str(image_id) + ".jpg"))
    if image_id in check_set:
        # Append to file files
        file = open(filename, 'a')
        file.write('\n')
        file.write(content)
        file.close()
    elif image_id not in check_set:
        check_set.add(image_id)
        # Write files
        file = open(filename, 'w+')
        file.write(content)
        file.close()


train_file = open(os.path.join(output_folder, 'train.txt'), 'a+')
val_file = open(os.path.join(output_folder, 'val.txt'), 'a+')
counter = 0
for image in os.listdir(os.path.join(output_folder, 'images')):
    counter += 1
    image_path = os.path.abspath(os.path.join(output_folder, 'images', image))
    if (counter == 4):
        counter = 0
        val_file.write(image_path + '\n')
    else:
        train_file.write(image_path + '\n')

train_file.close()
val_file.close()