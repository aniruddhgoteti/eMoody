
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import requests
import json
from requests import get
from wit import Wit

url = "http://192.168.1.33:54480/sony/audio"
headers = {'content-type': 'application/json'}

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + 'something')
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val

 
def handle_message(response):
    entities = response['entities']
    greetings = first_entity_value(entities, 'greetings')
    mood = first_entity_value(entities, 'mood')
    controls= first_entity_value(entities, 'controlSony')
    if controls:
        return volumeUp()
        return VolumeDown()
        return mute()
        return controllingSony()

    elif greetings:
        return 'Hi! You can say something like "I am feeling good"'
    else:
        return "Um. I don't recognize that name. " \
                "Which celebrity do you want to learn about?"    



def controllingSony():
# Example echo method
    payload = {
        "method":"setAudioMute",
        "id":601,
        "params":[
         {
          "mute":"on"
         }],
        "version":"1.1"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    
    print(response)

client = Wit(access_token= "62LAJRNXMDL4AEMTZE5AP34GAFMBF25R")
client.interactive(handle_message= handle_message)

