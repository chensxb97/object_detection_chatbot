## USAGE

**1. Download pre-trained yolov3 weights** 

Download [here](https://pjreddie.com/media/files/yolov3.weights) and store it as a *WEIGHTS* file in yolo-coco folder

**2. Social-distancing Detection on traffic camera videos**

python social_distance.py -i [VIDEO PATH] -o [OUTPUT PATH]

OUTPUT: Social distancing video analysis + Count/Violations & Avg Distance Diagrams

**3. Crowd Detection on traffic camera images**

python yolo_crowd.py -i [IMAGE PATH]

OUTPUT: Detected Image + Cluster Diagram

**4. Vehicle Detection on  traffic camera videos**

python social_distance.py -i [VIDEO PATH] -o [OUTPUT PATH]

OUTPUT: Social distancing video analysis + Count/Violations & Avg Distance Diagrams

**5. Vehicle Detection on traffic camera images**

python yolo_vehicle.py -i [IMAGE PATH]

OUTPUT: Detected Image + Cluster diagram
