import discord
import requests
import os
import sys
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO

client = discord.Client()
#IMPORTANT: For this bot to function, you must have a Microsoft Azure account and create a "Computer Vision" project
#and set two environmental vars: one for your key, one for the endpoint.

@client.event
async def on_message(message):

    if (message.author == client.user):
        return
    # Check to see if there are any attachments in the message sent
    if (len(message.attachments) != 0):
        
        # Go through each attachment in the message (if applicable)
        for attachment in message.attachments:        
            # Check to see if the attachment is an image
            if ('.jpeg' in attachment.url or '.png' in attachment.url):
                # Use Azure Computer Vision endpoint to determine if image is explicit
                if (azureEndpoint(attachment.url)):
                    # Delete the message if the endpoint deemed the image to be explicit
                   await message.delete()

def azureEndpoint(imageURL):
    # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()#Categories,Description,Color

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    analyze_url = endpoint + "vision/v2.1/analyze"

    # Set image_url to the URL of an image that you want to analyze.
   # image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/" + \
    #    "Broadway_and_Times_Square_by_night.jpg/450px-Broadway_and_Times_Square_by_night.jpg"
    image_url = imageURL 

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'visualFeatures': 'Adult'}
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers,
                            params=params, json=data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(json.dumps(response.json()))

    if (analysis["adult"]["isRacyContent"] == "true"):
        return True

    return False

client.run('PUT YOUR DISCORD BOT TOKEN HERE')
