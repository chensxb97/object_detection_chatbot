#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
derived from examples/bot-with-card-example-flask.py
"""
import os
import sys
from urllib.parse import urljoin
from flask import Flask, request, Response
from webexteamssdk import WebexTeamsAPI, Webhook

# Script metadata
__author__ = "JP Shipherd"
__author_email__ = "jshipher@cisco.com"
__contributors__ = ["Chris Lunsford <chrlunsf@cisco.com>"]
__copyright__ = "Copyright (c) 2016-2020 Cisco and/or its affiliates."
__license__ = "MIT"

# Constants
WEBHOOK_NAME = "botWithCardExampleWebhook"
WEBHOOK_URL_SUFFIX = "/events"
MESSAGE_WEBHOOK_RESOURCE = "messages"
MESSAGE_WEBHOOK_EVENT = "created"
CARDS_WEBHOOK_RESOURCE = "attachmentActions"
CARDS_WEBHOOK_EVENT = "created"

# Adaptive Card Design Schema for a sample form.
# To learn more about designing and working with buttons and cards,
# checkout https://developer.webex.com/docs/api/guides/cards
# https://developer.webex.com/buttons-and-cards-designer

detection_request_CARD = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "TextBlock",
            "text": "Object Detection Feature:",
            "size": "medium",
            "weight": "bolder"
        },
        {
            "type": "TextBlock",
            "text": "The **Object Detection** feature allows you to detect the instances of an interested object in **traffic-camera** images, at a specific location, with a comparison between an instance during **Covid-19** and **present day**. Bounding boxes are drawn over the image to identify the objects detected.",
            "wrap": True
        },
        {
            "type": "TextBlock",
            "text": "Please choose a **location**.",
            "wrap": True
        },
        { 

            "type": "Input.ChoiceSet",
            "id": "Location",
            "value": "Red",
            "choices": [
                {
                    "title": "Shibuya",
                    "value": "Shibuya"
                },
            ]
           
        },
        {
            "type": "TextBlock",
            "text": "Which **feature** do you want to analyse?",
            "wrap": True
        },
         { 

            "type": "Input.ChoiceSet",
            "id": "Feature",
            "value": "Red",
            "choices": [
                {
                    "title": "Crowd",
                    "value": "Crowd"
                },
                {
                    "title": "Vehicles",
                    "value": "Vehicles"
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "formDemoAction": "Submit"
            }
        }
    ]
}

detection_response_crowd_CARD = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "TextBlock",
            "text": "Object detection analysis",
            "size": "Large",
            "weight": "bolder",
            "horizontalAlignment": "center"
        },
        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_1",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "DATA_1",
            "wrap": True,
            "horizontalAlignment": "Center"      
        },
        {
            "type": "TextBlock",
            "text": "DATA_2",
            "wrap": True
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                "type": "Action.ShowCard",
                "title": "Cluster analysis",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                {
                            "type": "TextBlock",
                            "text": "Cluster analysis",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                {
                            "type": "TextBlock",
                            "text": "This section compares the degree of **clustering** between an instance during **Covid-19** and **present day**. Each cluster has at least **5 people** and is represented with a unique **color**.",
                            "size": "small",
                            "weight": "default",
                            "horizontalAlignment": 'left'
                },
            
                {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_2",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_3",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
        }
        ]    
        }
        },
                {
                "type": "Action.ShowCard",
                "title": "DATA_3",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                 {
                            "type": "TextBlock",
                            "text": "DATA_4",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                 {
                            "type": "TextBlock",
                            "text": "DATA_5",
                            "size": "small",
                            "weight": "default",
                },
                {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_4",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
            },
            {
                            "type": "TextBlock",
                            "text": "DATA_6",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                    },

                {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_5",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
            },
        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_7",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_8",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_6",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 new cases (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 deaths (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        ] 
        }
        }
            ],
            "horizontalAlignment": "Center",
            "spacing": "None"
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
}

detection_response_vehicles_CARD = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "TextBlock",
            "text": "Object detection analysis",
            "size": "Large",
            "weight": "bolder",
            "horizontalAlignment": "center"
        },
        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_1",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "DATA_1",
            "wrap": True,
            "horizontalAlignment": "Center"      
        },
        {
            "type": "TextBlock",
            "text": "DATA_2",
            "wrap": True
        },
        {
            "type": "ActionSet",
            "actions": [
                {
                "type": "Action.ShowCard",
                "title": "Cluster analysis",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                {
                            "type": "TextBlock",
                            "text": "Cluster analysis",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                {
                            "type": "TextBlock",
                            "text": "This section compares the degree of **clustering** between an instance during **Covid-19** and **present day**. Each cluster has at least **5 people** and is represented with a unique **color**.",
                            "size": "small",
                            "weight": "default",
                            "horizontalAlignment": 'left'
                },
            
                {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_2",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_3",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
        }
        ]    
        }
        },
                {
                "type": "Action.ShowCard",
                "title": "DATA_3",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                 {
                            "type": "TextBlock",
                            "text": "DATA_4",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                 {
                            "type": "TextBlock",
                            "text": "DATA_5",
                            "size": "small",
                            "weight": "default",
                },
                {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_4",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
            },

        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_6",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_7",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_5",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 new cases (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 deaths (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        ] 
        }
        }
            ],
            "horizontalAlignment": "Center",
            "spacing": "None"
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
}

aerial_detection_request_CARD = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "TextBlock",
            "text": "Aerial Object Detection Feature:",
            "size": "medium",
            "weight": "bolder"
        },
        {
            "type": "TextBlock",
            "text": "The **Aerial Object Detection** feature allows you to detect the instances of an interested object in **aerial** and/or **satellite images**, at a specific location, with a comparison between an instance during **Covid-19** and **present day**. Bounding boxes are drawn over the image to identify the objects detected.",
            "wrap": True
        },
        {
            "type": "TextBlock",
            "text": "Please choose a **location**.",
            "wrap": True
        },
        { 

            "type": "Input.ChoiceSet",
            "id": "Location",
            "value": "Red",
            "choices": [
                {
                    "title": "Haneda",
                    "value": "Haneda"
                },
                {
                    "title": "Miscellanous",
                    "value": "Miscellanous"
                }
            ]
           
        },
        {
            "type": "TextBlock",
            "text": "Which **feature** do you want to analyse?",
            "wrap": True
        },
         { 

            "type": "Input.ChoiceSet",
            "id": "Feature",
            "value": "Red",
            "choices": [
                {
                    "title": "Planes",
                    "value": "Planes"
                },
                {
                    "title": "Vehicles",
                    "value": "Vehicles"
                }
                
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit",
            "data": {
                "formDemoAction": "Submit"
            }
        }
    ]
}

aerial_detection_response_CARD = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "TextBlock",
            "text": "Aerial Object Detection analysis",
            "size": "Large",
            "weight": "bolder",
            "horizontalAlignment": "center"
        },
        {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_1",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "DATA_1",
            "wrap": True,
            "horizontalAlignment": "Center"      
        },
        {
            "type": "TextBlock",
            "text": "DATA_2",
            "wrap": True
        },
         {
            "type": "ActionSet",
            "actions": [
                {
                "type": "Action.ShowCard",
                "title": "Cluster analysis",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                {
                            "type": "TextBlock",
                            "text": "Cluster analysis",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                {
                            "type": "TextBlock",
                            "text": "This section compares the degree of **clustering** between an instance during **Covid-19** and **present day**. Each cluster has at least **10 detections** and is represented with a unique **color**.",
                            "size": "small",
                            "weight": "default",
                            "horizontalAlignment": 'left'
                },
            
                {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_2",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Random day in March 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "Image",
                            "style": "default",
                            "url": "IMAGE_3",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
                
        },
        {
                            "type": "TextBlock",
                            "text": "Friday, 17 July 2020",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
        }
        ]    
        }
        },
                {
                "type": "Action.ShowCard",
                "title": "Traffic & Covid-19 analysis",
                "card": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.1",
                "body": [
                 {
                            "type": "TextBlock",
                            "text": "Traffic & Covid-19 analysis",
                            "size": "Large",
                            "weight": "bolder",
                            "horizontalAlignment": 'Center'
                },
                 {
                            "type": "TextBlock",
                            "text": "This section offers insights on the **traffic conditions** as well as trends in daily **Covid-19 new cases** and **deaths** updated in **real time**.",
                            "size": "small",
                            "weight": "default",
                },
                {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_4",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
        },
        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_3",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "DATA_4",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        {
                            "type": "Image", 
                            "style": "default",
                            "url": "IMAGE_5",
                            "size": "Medium",
                            "height": "150px",
                            "horizontalAlignment": "center"
        },
        {
            "type": "ColumnSet",
            "columns": [

                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 new cases (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 35,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Trend of Covid-19 deaths (daily)",
                            "size": "small",
                            "weight": "bolder",
                            "horizontalAlignment": "Center"       
                        }
                    ]        
                }
            ]
           # "spacing": "Padding",
           # "horizontalAlignment": "Center"
        },
        ] 
        }
        }
            ],
            "horizontalAlignment": "Center",
            "spacing": "None"
        }
    ],
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
}

# Module variables
webhook_url = os.environ.get("WEBHOOK_URL", "")
port = int(os.environ.get("PORT", 0))
access_token = os.environ.get("WEBEX_TEAMS_ACCESS_TOKEN", "")
if not all((webhook_url, port, access_token)):
    print(
        """Missing required environment variable.  You must set:
        * WEBHOOK_URL -- URL for Webex Webhooks (ie: https://2fXX9c.ngrok.io)
        * PORT - Port for Webhook URL (ie: the port param passed to ngrok)
        * WEBEX_TEAMS_ACCESS_TOKEN -- Access token for a Webex bot
        """
    )
    sys.exit()

# Initialize the environment
# Create the web application instance
flask_app = Flask(__name__)
# Create the Webex Teams API connection object
api = WebexTeamsAPI()
# Get the details for the account who's access token we are using
me = api.people.me()
shared_dir = os.getcwd() + "/shared"
# for debug
import inspect
def debug_object(obj, prefix="==>"):
    print(f"{prefix} {type(obj)}")
    print(f"{str(obj)}")
    maxlen = max([len(i) for i in dir(obj) if not i.startswith("_")])
    for i in dir(obj):
        if not i.startswith("_"):
            attr = eval(f"obj.{i}")
            t = str(type(attr))
            print(f"  {i.ljust(maxlen)}: {t}")
            if "str" in t:
                print(f"    {attr}")
            elif "dict" in t:
                for k,v in attr.items():
                    print(f"    {k}: {v}")
            elif "method" in t:
                print(f"    {inspect.getfullargspec(attr)}")
            else:
                pass

import base64
def encode_local_data(filename, ctype="image/png"):
    # data URL is defined in RFC 2397
    # the value should be formed;
    #     "data:[<media type>][;base64],<data>"
    return "data:{};base64,{}".format(ctype, base64.b64encode(
            open(filename,"rb").read()).decode("utf-8"))

import copy

def putval(content, key, val, target="__DATA1__", encode=False, ctype=None,
           stored=True):
    """replace into val from target of key in content.
    return content replaced if sucessful, or return None if faild.
    note that it modifies content directly.
    you have to store it before calling this function.
    """
    if stored:
        _c = copy.deepcopy(content)
    else:
        _c = content
    def lookup_dict(d):
        for k,v in d.items():
            if k == key and v == target:
                if encode:
                    d.update({ k: encode_local_data(val, ctype) })
                else:
                    d.update({ k: val })
                return True
            elif isinstance(v, dict):
                if lookup_dict(v):
                    return True
            elif isinstance(v, list):
                for j in v:
                    if lookup_dict(j):
                        return True
        return False
    #
    ret = lookup_dict(_c)
    if ret:
        return _c
    else:
        return None

def putvals(content, vals, stored=True):
    """replace into each val from target of key in content.
    valus must a list of below items:
        {
            "key":key,
            "val":val,
            "target":"__DATA1__",
            "ctype":None,
            "ctype":ctype
        }
    """
    if stored:
        _c = copy.deepcopy(content)
    else:
        _c = content
    for x in vals:
        _c = putval(_c, x["key"], x["val"], target=x.get("target"),
                     encode=x.get("encode"), ctype=x.get("ctype"))
        if _c is None:
            return None
    return _c


def finish_interaction(room, message_id, attachment):

    """
    # Data URI Scheme is not supported yet. (26-Jun-2020)
    attachment = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": put_local_data("bot-test.png", CARD_CONTENT3)
        }
    api.messages.create(
        room.id,
        parentId=message_id,
        text="If you see this your client cannot render cards",
        attachments=[attachment],
    )
    """
    api.messages.create(roomId=room.id, files=[os.path.abspath("bot-test.png")])

def receiving_period(webhook, input_data):
    """Respond to a message to the username submission"""
    print("start_date=", input_data.get("start_date"))
    print("end_date=", input_data.get("end_date"))
    return True

def receiving_username(webhook, input_data):
    """Respond to a message to the username submission"""
    print("username=", input_data.get("username"))
    return True

def cards_handler(webhook):
    room = api.rooms.get(webhook.data.roomId)
    attachment = api.attachment_actions.get(webhook.data.id)
    person = api.people.get(attachment.personId)
    message_id = attachment.messageId
    print(f"""
          room={room.title}
          person={person.displayName}
          message_id={message_id}
          attachment_action={attachment}
          """)

    input_info = dict(attachment.json_data['inputs'])
    location = input_info['Location']
    feature = input_info['Feature']

    if detection(input_info)=='traffic':
        api.messages.create(
                room.id, 
                markdown="Request submitted for *Object Detection Feature*" 
                )
        if feature == 'Crowd' and location == 'Shibuya': 
            content = putvals(detection_response_crowd_CARD, [
                    {
                        "key": "url",
                        "target": "IMAGE_1",
                        "val": f"{webhook_url}/xdoc/traffic/crowd/Shibuya/combined.jpg",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_2",
                        "val": f"{webhook_url}/xdoc/traffic/crowd/Shibuya/covid_graph.png",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_3",
                        "val": f"{webhook_url}/xdoc/traffic/crowd/Shibuya/present_graph.png",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_4",
                        "val": f"{webhook_url}/xdoc/traffic/crowd/Shibuya/detected_images/image21.jpg",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_5",
                        "val": f"{webhook_url}/xdoc/traffic/crowd/Shibuya/sd_summary.png",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_6",
                        "val": f"{webhook_url}/xdoc/data/covid/combined.jpg",
                    },
                    {
                        "key": "text",
                        "target": "DATA_1",
                        "val": f"**The Shibuya Crossing, Tokyo, Japan**",
                    },
                    {
                        "key": "text",
                        "target": "DATA_2",
                        "val": f"**Shibuya Crossing** or **Shibuya Scramble Crossing** is located in front of the Shibuya Station Hachikō exit and stops vehicles in all directions to allow pedestrians to inundate the entire intersection. It is estimated that Shibuya Station handles an average of over **2.4 million** passengers each day and **2,500** people crossing the intersection at a time. With the lockdown, these numbers are expected to drop significantly.",
                    },
                    {
                        "key": "title",
                        "target": "DATA_3",
                        "val": f"Social-distancing & Covid-19 analysis",
                    },
                    {
                        "key": "text",
                        "target": "DATA_4",
                        "val": f"Social-distancing & Covid-19 analysis",
                    },
                    {
                        "key": "text",
                        "target": "DATA_5",
                        "val": f"**Social-distancing** is a safety measure to reduce the spread of contagious viruses under severe circumstances. The following analysis measures the relative distance between each detection during an instance in **present day**. Detections which violate the minimum distance of **1.8m** will be highlighted in **red**. This analysis also includes trends in daily **Covid-19 new cases** and **deaths** updated in **real time**.",
                    },
                    {
                        "key": "text",
                        "target": "DATA_6",
                        "val": f"Video analysis of social distancing violations\nTaken on Friday, 17 July 2020, 6:23PM(GMT+9)",
                    },
                    {
                        "key": "text",
                        "target": "DATA_7",
                        "val": f"Detections & Violations",
                    },
                    {
                        "key": "text",
                        "target": "DATA_8",
                        "val": f"Average distance between detections",
                    },
                    ])
        elif feature == 'Vehicles' and location == 'Shibuya':
            content = putvals(detection_response_vehicles_CARD, [
                    {
                        "key": "url",
                        "target": "IMAGE_1",
                        "val": f"{webhook_url}/xdoc/traffic/vehicles/Shibuya/combined1.jpg",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_2",
                        "val": f"{webhook_url}/xdoc/traffic/vehicles/Shibuya/covid_graph.png",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_3",
                        "val": f"{webhook_url}/xdoc/traffic/vehicles/Shibuya/present_graph.png",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_4",
                        "val": f"{webhook_url}/xdoc/traffic/vehicles/Shibuya/combined2.jpg",
                    },
                    {
                        "key": "url",
                        "target": "IMAGE_5",
                        "val": f"{webhook_url}/xdoc/data/covid/combined.jpg",
                    },
                    {
                        "key": "text",
                        "target": "DATA_1",
                        "val": f"**The Shibuya Route, Tokyo, Japan**",
                    },
                    {
                        "key": "text",
                        "target": "DATA_2",
                        "val": f"**The Shibuya Route** (渋谷線, Shibuya-sen), signed as **Route 3**, is one of the radial routes of the Shuto Expressway system in Tokyo. **Route 3** runs southwest from Tanimachi Junction (with the Inner Circular Route) in Minato-ku and runs for **12 kilometers** through Shibuya-ku, Meguro-ku, and Setagaya-ku.",
                    },
                    {
                        "key": "title",
                        "target": "DATA_3",
                        "val": f"Traffic & Covid-19 analysis",
                    },
                    {
                        "key": "text",
                        "target": "DATA_4",
                        "val": f"Traffic & Covid-19 analysis",
                    },
                    {
                        "key": "text",
                        "target": "DATA_5",
                        "val": f"This section offers insights on the **traffic conditions** as well as trends in daily **Covid-19 new cases** and **deaths** updated in **real time**.",
                    },
                    {
                        "key": "text",
                        "target": "DATA_6",
                        "val": f"Count vs Time",
                    },
                    {
                        "key": "text",
                        "target": "DATA_7",
                        "val": f"Video analysis of vehicle detections\nTaken on Friday, 15 July 2020, 6:34PM(GMT+9)",
                    },
                    ])
        else:
            content = None

    elif detection(input_info) == 'aerial':
        api.messages.create(
                room.id, 
                markdown="Request submitted for *Aerial Object Detection Feature*" 
                )
        if feature =='Vehicles' and location == 'Miscellanous':
            content = putvals(aerial_detection_response_CARD, [
                {
                    "key": "url",
                    "target": "IMAGE_1",
                    "val": f"{webhook_url}/xdoc/aerial/vehicles/Miscellanous/combined.jpg",
                },
                {
                    "key": "url",
                    "target": "IMAGE_2",
                    "val": f"{webhook_url}/xdoc/aerial/vehicles/Miscellanous/covid_graph.png",
                },
                {
                    "key": "url",
                    "target": "IMAGE_3",
                    "val": f"{webhook_url}/xdoc/aerial/vehicles/Miscellanous/present_graph.png",
                },
                {
                    "key": "url",
                    "target": "IMAGE_4",
                    "val": f"{webhook_url}/xdoc/data/vehicles/combined.jpg",
                },
                {
                    "key": "url",
                    "target": "IMAGE_5",
                    "val": f"{webhook_url}/xdoc/data/covid/combined.jpg",
                },
                {
                    "key": "text",
                    "target": "DATA_1",
                    "val": f"**A random parking lot**",
                },
                {
                    "key": "text",
                    "target": "DATA_2",
                    "val": f"A test image for aerial vehicle detection",
                },
                {
                    "key": "text",
                    "target": "DATA_3",
                    "val": f"Trend in traffic congestion (Hourly)",
                },
                {
                    "key": "text",
                    "target": "DATA_4",
                    "val": f"Trend in traffic congestion (Weekly)",
                }
                ])
        elif feature =='Planes' and location == 'Haneda':
            content = putvals(aerial_detection_response_CARD, [
            {
                "key": "url",
                "target": "IMAGE_1",
                "val": f"{webhook_url}/xdoc/aerial/planes/Haneda/combined.jpg",
            },
            {
                "key": "url",
                "target": "IMAGE_2",
                "val": f"{webhook_url}/xdoc/aerial/planes/Haneda/covid_graph.png",
            },
            {
                "key": "url",
                "target": "IMAGE_3",
                "val": f"{webhook_url}/xdoc/aerial/planes/Haneda/present_graph.png",
            },
            {
                "key": "url",
                "target": "IMAGE_4",
                "val": f"{webhook_url}/xdoc/data/planes/combined.jpg",
            },
            {
                "key": "url",
                "target": "IMAGE_5",
                "val": f"{webhook_url}/xdoc/data/covid/combined.jpg",
            },
            {
                "key": "text",
                "target": "DATA_1",
                "val": f"**Haneda Airport**",
            },
            {
                "key": "text",
                "target": "DATA_2",
                "val": f"**Haneda Airport** (羽田空港, Haneda Kūkō, HND), formally known as **Tokyo International Airport**, is located less than 30 minutes south of central Tokyo. Compared to Narita Airport, Haneda Airport handles significantly **more domestic flights**, but fewer international flights. With over **80 million** passengers per year overall, Haneda Airport is currently **Japan's busiest airport**.",
            },
            {
                "key": "text",
                "target": "DATA_3",
                "val": f"Trend in passenger traffic (Monthly)",
            },
            {
                "key": "text",
                "target": "DATA_4",
                "val": f"Trend in passenger traffic (Yearly)",
            }
            ])
        else:
            content = None

    if content is None:
        api.messages.create(
                room.id,
                text="No information available at the requested location",
            )
        return "ERROR", 500
    else:
        api.messages.create(
            room.id, 
            text="Retrieving information from our database..."
        )
        ret = api.messages.create(
            roomId=room.id,
            text="If you see this your client cannot render cards",
            attachments=[{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": content
                }],
            )
        debug_object(ret)

def message_handler(webhook):
    """Respond to a message to our bot"""
    room = api.rooms.get(webhook.data.roomId)
    message = api.messages.get(webhook.data.id)
    person = api.people.get(message.personId)
    print(f"""
          room={room.title}
          person={person.displayName}
          message={message.text}
          """)

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    if message.personId == me.id:
        # Message was sent by me (bot); do not respond.
        return "OK"
    # others
    elif message.text == "/detection":
        api.messages.create(
                room.id,
                text="If you see this your client cannot render cards",
                attachments=[{
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": detection_request_CARD
                }]
            )
    elif message.text == "/aerial-detection":
        api.messages.create(
                room.id,
                text="If you see this your client cannot render cards",
                attachments=[{
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": aerial_detection_request_CARD
                }]
            )
# Core bot functionality
# Webex will post to this server when a message is created for the bot
# or when a user clicks on an Action.Submit button in a card posted by this bot
# Your Webex Teams webhook should point to http://<serverip>:<port>/events
@flask_app.route("/events", methods=["POST"])
def webex_teams_webhook_events():
    """Respond to inbound webhook JSON HTTP POST from Webex Teams."""
    # Create a Webhook object from the JSON data
    webhook_obj = Webhook(request.json)

    # Handle a new message event
    if (webhook_obj.resource == MESSAGE_WEBHOOK_RESOURCE
            and webhook_obj.event == MESSAGE_WEBHOOK_EVENT):
        message_handler(webhook_obj)

    # Handle an Action.Submit button press event
    elif (webhook_obj.resource == CARDS_WEBHOOK_RESOURCE
          and webhook_obj.event == CARDS_WEBHOOK_EVENT):
        cards_handler(webhook_obj)

    # Ignore anything else (which should never happen
    else:
        print(f"IGNORING UNEXPECTED WEBHOOK:\n{webhook_obj}")

    return "OK"

@flask_app.route("/xdoc/<path:path>", methods=["GET"])
def webex_teams_providing_documents(path):
    mimetypes = {
        ".png": "image/png",
        ".jpg": "image/jpg",
        ".gif": "image/gif",
    }
    mimetype = mimetypes.get(os.path.splitext(path)[1])
    if mimetype is None:
        return "ERROR", 404
    try:
        content = open(os.path.join(shared_dir, path), "rb").read()
    except IOError as exc:
        return "ERROR", 404
    return Response(content, mimetype=mimetype)

# Helper functions
def detection(input_info): #Returns a list of [image paths]+[descriptions]
    location = input_info['Location']
    feature= input_info['Feature']
    mode = None
    if location == 'Shibuya':
        mode = 'traffic'
    elif location in ['Miscellanous','Haneda']:
        mode = 'aerial'
    return mode

def delete_webhooks_with_name():
    """List all webhooks and delete webhooks created by this script."""
    for webhook in api.webhooks.list():
        if webhook.name == WEBHOOK_NAME:
            print("Deleting Webhook:", webhook.name, webhook.targetUrl)
            api.webhooks.delete(webhook.id)


def create_webhooks(webhook_url):
    """Create the Webex Teams webhooks we need for our bot."""
    print("Creating Message Created Webhook...")
    webhook = api.webhooks.create(
        resource=MESSAGE_WEBHOOK_RESOURCE,
        event=MESSAGE_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")

    print("Creating Attachment Actions Webhook...")
    webhook = api.webhooks.create(
        resource=CARDS_WEBHOOK_RESOURCE,
        event=CARDS_WEBHOOK_EVENT,
        name=WEBHOOK_NAME,
        targetUrl=urljoin(webhook_url, WEBHOOK_URL_SUFFIX)
    )
    print(webhook)
    print("Webhook successfully created.")


def main():
    # Delete preexisting webhooks created by this script
    delete_webhooks_with_name()

    create_webhooks(webhook_url)

    try:
        # Start the Flask web server
        flask_app.run(host="0.0.0.0", port=port)

    finally:
        print("Cleaning up webhooks...")
        delete_webhooks_with_name()


if __name__ == "__main__":
    main()
