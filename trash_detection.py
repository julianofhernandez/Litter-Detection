import argparse
from src.yolo_pretrained_on_coco import YoloPretrainedOnCoco


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')
	detect = subparser.add_parser('detect')

	detect.add_argument('--image', type=str, required=True)
	detect.add_argument('--detector', type=str, required=True)
	args = parser.parse_args()

	if (args.command == 'detect'):
		detector = YoloPretrainedOnCoco()
		# detector.image_detect("datasets/smart_water_bottle.jpg")
		detector.image_detect(args.image)
