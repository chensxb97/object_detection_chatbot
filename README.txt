Object Detection Chatbot

This directory contains files and folders to set up a local environment to run the object detection chatbot using webexteamssdk.

shared* is the database that holds the pre-processed images that will be utilised by the chatbot. It also contains a folder of detection algorithms 
with instructions on how to use them.

requirements.txt* show the list of packages to be installed.

test.py* is the chatbot python file.


1. Clone repo

- git clone 

2. Open terminal and install dependencies

- pip install -r requirements.txt

3. Install ngrok and run it on a separate terminal

- Copy the url under 'Forwarding', which will be stored as WEBHOOK_URL in environment variables

4. Set environment variables

PORT = 8080
WEBEX_TEAMS_ACCESS_TOKEN = [token can be obtained when creating a new bot by following instructions on https://developer.webex.com/docs/bots]
WEBHOOK_URL = [Copied previously in 3.]

5. Run chatbot python file

- 'python test.py'
