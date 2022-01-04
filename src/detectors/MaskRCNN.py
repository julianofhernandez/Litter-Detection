import os
import sys
import warnings
import skimage.io
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn.config import Config

class MaskRCNN:
    def __init__(self, weights="", config="", confidence=0.3):
        weights = "models/mask_rcnn_taco.h5"
        self.confidence=confidence
        self.weights = weights
        # COCO Class names
        self.class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
                    'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
                    'fork', 'knife', 'spoon', 'bowl', 'bananas', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
                    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                    'teddy bear', 'hair drier', 'toothbrush']
        # self.model_path = "/models/mask_rcnn_taco.h5"
        warnings.filterwarnings("ignore")

        # Local path to trained weights file
        COCO_MODEL_PATH = os.path.join('', "mask_rcnn_taco.h5")

        # Download COCO trained weights from Releases if needed
        if not os.path.exists(weights):
            utils.download_trained_weights(weights)

        class InferenceConfig(Config):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            NAME = "coco"
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1

        config = InferenceConfig()

        # Create model object in inference mode.
        self.model = modellib.MaskRCNN(mode="inference", model_dir='meaninglessdata', config=config)

        # Load weights trained on MS-COCO
        self.model.load_weights(weights, by_name=True)


    def format_output(self, class_ids, scores):
        # Scrores are passed for use later, but for now they can just stay
        properties = {}
        for i in range(len(scores)):
            if scores[i] > self.confidence:
                label = self.class_names[class_ids[i]]
                try:
                    properties[label] += 1
                except KeyError:
                    properties[label] = 1
        return [properties]

    def detect(self, image_path):
        # Load a random image from the images folder
        image = skimage.io.imread(image_path)

        # Run detection
        results = self.model.detect([image], verbose=0)

        # Visualize results
        r = results[0]
        return self.format_output(r['class_ids'], r['scores'])
