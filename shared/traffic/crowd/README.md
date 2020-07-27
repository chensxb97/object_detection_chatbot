#### How this folder was made

1) Extract raw image frames from video using video_to_image.py

2) Perform detection on start and end frames using yolo_crowd.py to generate the 2 detected images and cluster plots

3) Use concatenate_image.py on the two detected images to create combined.jpg

4) Perform detection on the raw video using social_distance.py to generate detection summary analysis plot

5) Extract frames from social distancing analysis video using video_to_image.py and store them in detected_images

