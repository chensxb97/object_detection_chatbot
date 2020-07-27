#Convert video freames to images

import cv2
import argparse
from PIL import Image
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help="path to video")
args = vars(ap.parse_args())

vidcap = cv2.VideoCapture(args['video'])
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image"+str(count)+".jpg", image) # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 1 #//it will capture image in each 0.5 second
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)