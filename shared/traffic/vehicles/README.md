### How this folder was made

1) Extract raw image frames from video using video_to_image.py

2) Perform detection on start and end frames using yolo_vehicle.py to generate the 2 detected images and cluster plots

3) Perform detection on the video using yolo_vehicle_video.py to generate detection summary analysis plot

4) Extract frames from detection analysis video using video_to_image.py and store them in detected_images

5) Use concatenate.py on the [2 detected images to create combined1.jpg] and on the [detection_summary analysis plot + a random detected_image to create combined2.jpg]. 

