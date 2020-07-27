## Object_detection_chatbot
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This project involves using object detection algorithms to analyse the changes in crowd, vehicle and flight traffic on traffic-camera and aerial images to understand the urban impact caused by Covid-19. Pre-processed images are integrated with a Webex Teams Chatbot which aims to educate and inform the public on COVID-19 related insights.

## Table of Content
- [Motivation](#motivation)
- [Installation](#installation)
  * [Step 1: Creating a virutal environment](#step-1--creating-a-virtual-environment)
  * [Step 2: Install webexteamssdk](#step-2--install-webexteamssdk)
  * [Step 3: Create your bot on Cisco Webex](#step-3--create-your-bot-on-cisco-webex)
  * [Step 4: Setup ngrok and env variables](#step-4--setup-ngrok-and-env-variables)
  * [Step 5: Run the bot](#step-5--run-the-bot)
- [Features](#features-)
  * [Object detection feature](#object-detection-feature)
  * [Aerial object detection feature](#aerial-object-detection-feature)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
  * [Real-time data](#real-time-data)
  * [Direct-integration of detection algorithms](#integration)
  * [Accuracy](#accuracy)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Motivation
Given the impact this recent pandemic has had on our world, we decided to create a chatbot to help both the common public and decision makers alike through the features we have implemented.

## Installation
The following dependencies need to be installed before running the chatbot. I managed to execute the chatbot using the Anaconda Prompt on Windows OS, but feel free to use Linux/Ubuntu whichever you prefer. The following are items this documentation assumes you already have installed: 
- virtualenv 
- python3 
- [ngrok](https://ngrok.com/download)

### Step 1: Creating a virtual environment
Initialize the virtual environment by running the following commands in your local terminal

```sh
virtualenv venv
source venv/bin/activate
```
### Step 2: Install webexteamssdk
You now have your virtual environment set up. We next need the webexteamssdk module to run the chatbot in python.

```sh
pip install webexteamsssdk
```
### Step 3: Create your bot on Cisco Webex
If you have already created your bot, move on to step 4 with your **access token**. Else, create your Webex Account and create your bot. You will be given an access token. Be sure to save it somewhere safe. We will need it in step 4.

### Step 4: Setup ngrok and env variables
In a different terminal, navigate to the folder where you have the ngrok placed and run the following command.
```sh
ngrok http 5000
```
You should see a url of _https://...ngrok.io_ format. Copy it and export it to the env variables. 
Also, export the port used for ngrok. In this case, we used port 5000. 
```sh
export WEBHOOK_URL=https://...ngrok.io
export PORT=5000
```
Finally, take your bot's access token and place it in your environment variable as WEBEX_TEAMS_ACCESS_TOKEN.

### Step 5: Requirements.txt

```sh
pip install -r requirements.txt
```

### Step 6: Run bot

We can now run the bot.
```sh
python ./test.py
```
## Features!
We will cover the additional 2 features here:
* Object detection feature
* Aerial object detection feature

The first three features were covered previously [here](https://github.com/shawnlim97/CiscoCovidBot-Final-)
### Object detection feature
The **Object detection feature** is activated using the /detection keyword command with the card as shown 

![Screenshot](Screenshots/compare_response.png)

Once submitted, the bot will access the shared dir to obtain the necessary pre-processed images and secondary data for analysis.

Example object detection feature response:

![Screenshot](Screenshots/comparecard.png)

*Detecting object: **Crowd** in the location: **Shibuya**

### Aerial Object detection feature
The **aerial detection feature** is activated using the /aerial-detection keyword command with the card as shown 

![Screenshot](Screenshots/compare_response.png)

Once submitted, the bot will access the shared dir to obtain the necessary pre-processed images and secondary data for analysis.

Example of aerial object detection feature response:

![Screenshot](Screenshots/comparecard.png)

*Detecting object: planes in the location: Haneda.

