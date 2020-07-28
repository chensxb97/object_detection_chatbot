#Pre-detect images via yolo and storing the new images into the database 
#According to the country, location, feature
from PIL import Image
import re
import os
import glob
import cv2

def create_detected_images():             
    images_path = r'C:\Users\Benedict\cisco_projects\database\TF_car\images'
    print(images_path)
    images_list= [file for file in os.listdir(images_path) if file.endswith('.jpg')] #Image names
    print(images_list)
    for image in images_list:
    	#DETECT PLANE
    	#annotation=image.replace('jpg','txt')
    	#os.system('python detect_plane.py -i images_raw/{} -a images_raw/{}'.format(image,annotation))

    	#DETECT CROWD
    	#os.system('python yolo_crowd.py -i images_raw/{} -y yolo-coco'.format(image))

    	#DETECT VEHICLE
    	#os.system('python detect_car.py -i {}'.format(image))

create_detected_images()



