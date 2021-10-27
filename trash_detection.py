import argparse
from src.yolo_pretrained_on_coco import YoloPretrainedOnCoco


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')
	detect = subparser.add_parser('detect')

	detect.add_argument('-i', '--image', type=str, required=True, help='The path to the image you want to process')
	detect.add_argument('-m', '--model', type=str, help='Which bject detection model to use')
	args = parser.parse_args()

	if (args.command == 'detect'):
		detector = YoloPretrainedOnCoco()
		detector.image_detect(args.image)
