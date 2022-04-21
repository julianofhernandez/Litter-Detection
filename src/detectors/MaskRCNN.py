import os
import sys
import warnings
import skimage.io

ROOT_DIR = os.path.abspath("C:\\Users\\julian\\repos\\McNair-Project\\src\\TACO\\detector")
sys.path.append(ROOT_DIR)

# from mrcnn import utils
# import mrcnn.model as modellib
# from mrcnn.config import Config

import os
import csv
import random

from dataset import Taco
import model as modellib
from model import MaskRCNN as MaskRCNNLib
from config import Config
import visualize
import utils
import matplotlib.pyplot as plt
import skimage
import numpy as np


# Root directory of the models
ROOT_DIR = os.path.abspath(".\TACO\detector\models")

# Path to trained weights file
TACO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_taco_0100.h5")

# Directory to save logs and model checkpoints
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

class MaskRCNN:
    def __init__(self, modelDir, confidence):
        modelPath=TACO_MODEL_PATH
        round=0
        class_map_path='./TACO/detector/taco_config/map_10.csv'
        dataset='./TACO/data'
        self.confidence = confidence

        # Read map of target classes
        class_map = {}
        map_to_one_class = {}
        with open(class_map_path) as csvfile:
            reader = csv.reader(csvfile)
            class_map = {row[0]: row[1] for row in reader}
            map_to_one_class = {c: 'Litter' for c in class_map}

        # Test dataset
        dataset_test = Taco()
        taco = dataset_test.load_taco(dataset, round, "test", class_map=class_map, return_taco=True)
        dataset_test.prepare()
        nr_classes = dataset_test.num_classes
        print('Number of classes: ' + str(nr_classes))

        # Configurations
        class TacoTestConfig(Config):
            NAME = "taco"
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
            DETECTION_MIN_CONFIDENCE = 30
            NUM_CLASSES = nr_classes
            USE_OBJECT_ZOOM = False
        config = TacoTestConfig()
        config.display()

        model = MaskRCNNLib(mode="inference", config=config, model_dir=DEFAULT_LOGS_DIR)
        model_path = TACO_MODEL_PATH
        model.load_weights(model_path, model_path, by_name=True)
        self.model = model
        self.dataset=dataset_test
        self.config = config
        # return model, dataset_test, config

    def detect(self, image_path, save_path=None):
        model = self.model
        dataset = self.dataset
        config = self.config

        nr_images = len(dataset.image_ids)
        image_id = dataset.image_ids[1] if nr_images == len(dataset.image_ids) else random.choice(dataset.image_ids)

        image = skimage.io.imread(fname=image_path)
        # If grayscale. Convert to RGB for consistency.
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        # If has an alpha channel, remove it for consistency
        if image.shape[-1] == 4:
            image = image[..., :3]

        r = model.detect([image], verbose=0)[0]

        print(r['class_ids'].shape)
        if r['class_ids'].shape[0]>0:
            r_fused = utils.fuse_instances(r)
        else:
            r_fused = r

        fig, ax = plt.subplots(1, 1, figsize=(16, 16))

        visualize.display_instances(image, r_fused['rois'], r_fused['masks'], r_fused['class_ids'],
                                        dataset.class_names, r_fused['scores'], title="Image Predictions", ax=ax)
        results = self.format_output(r_fused)
        # print('Saving image to ' + save_path)
        plt.savefig(save_path)
        plt.cla()
        plt.close(fig)
        return results

    def format_output(self, results):
        properties = {}
        N = results['rois'].shape[0]
        for i in range(N):
            class_id = results['class_ids'][i]
            score = results['scores'][i] if results['scores'] is not None else None
            label = self.dataset.class_names[class_id]
            if (score > self.confidence):
                try:
                    properties[label] += 1
                except KeyError:
                    properties[label] = 1
        return properties
