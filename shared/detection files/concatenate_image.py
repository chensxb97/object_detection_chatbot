import argparse
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-i1", "--image1", required=True,
    help="path to image1")
ap.add_argument("-i2", "--image2", required=True,
    help="path to image2")

args = vars(ap.parse_args())

im1 = cv2.imread(args['image1'])
im2 = cv2.imread(args['image2'])
im_h = cv2.hconcat([im1, im2])
cv2.imwrite('combined.jpg', im_h)