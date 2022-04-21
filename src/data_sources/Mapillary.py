import requests
import json
import urllib.request
import os
from tqdm import tqdm

class Mapillary:
    def __init__(self):
        # TODO: This should be encrypted
        self.access_token = 'MLY|3461141010677895|c26e4e4b32b90d5cb1db934c54ebe2c8'
        self.image_folder = 'images'

    def get_coordinates(self, id):
        '''Get coordinates for an image given an ID'''
        responce = requests.get(f'https://graph.mapillary.com/{id}?access_token={self.access_token}&fields=id,computed_geometry')
        responce_json = json.loads(responce.content.decode('utf-8'))
        coordinates = responce_json['computed_geometry']['coordinates']
        return coordinates

    def download_image(self, id):
        '''Download image based on ID'''
        # Downloads the image to id.
        responce = requests.get(f'https://graph.mapillary.com/{id}?access_token={self.access_token}&fields=thumb_1024_url')
        responce_json = json.loads(responce.content.decode('utf-8'))
        url = responce_json['thumb_1024_url']
        urllib.request.urlretrieve(url,os.path.join('images', 'mapillary', str(id) + '.png'))

    def download_images_in_bbox(self,minx,miny,maxx,maxy):
        '''Downloads all images in a given bounding box from Mapillary'''
        # Downloads the image to id.
        responce = requests.get(f'https://graph.mapillary.com/images?access_token={self.access_token}&fields=id&bbox={minx},{miny},{maxx},{maxy}')
        responce_json = json.loads(responce.content.decode('utf-8'))
        total_images = len(responce_json['data'])
        print(f'Downloading {total_images} images')
        for i in tqdm(range(total_images)):
            id = responce_json['data'][i]['id']
            self.download_image(id)
