from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import requests
import json
from requests import get
from wit import Wit
import time
from pygame import mixer
from Recorder import record_audio, read_audio

API_ENDPOINT = 'https://api.wit.ai/speech'

url = "http://192.168.2.62:54480/sony/audio"
url1 = "http://192.168.2.62:54480/sony/system"
headers = {'content-type': 'application/json'}

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + 'KXHAFEIGLTH7TNZ2IG4IGM3J32J6O65X')
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return ""
    val = entities[entity][0]['value']
    if not val:
        return ""
    return val
	
	
def RecognizeSpeech(AUDIO_FILENAME, num_seconds = 5):
    
	
   
   # record audio of specified length in specified audio file
    record_audio(num_seconds, AUDIO_FILENAME)
    
    # reading audio
    audio = read_audio(AUDIO_FILENAME)
    
    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + access_token,
               'Content-Type': 'audio/wav'}

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers = headers,
                         data = audio)
    
    # converting response content to JSON format
    data = json.loads(resp.content)
    
    # get text from data
    text = data['_text']
    
    # return the text
    return text

 
def handle_message(response):
    entities = response['entities']
    greet = first_entity_value(entities, 'greetings')
    moodH = first_entity_value(entities, 'moodHappy')
    mute= first_entity_value(entities, 'controlVolumeMute')
    muteoff= first_entity_value(entities, 'controlVolumeMuteOff')
    moodS= first_entity_value(entities, 'moodSad')
    shutdown= first_entity_value(entities, 'controlShutDown')
    frust= first_entity_value(entities, 'Frustrated')
    poweron= first_entity_value(entities, 'controlPower')

    if greet:
        return "Hi There"
    elif moodS:
        return moodSad()
    elif moodH:
        return moodHappy()
    elif mute: 	
        return controlVolumeMute()
    elif muteoff:
        return controlVolumeMuteOff()
    elif frust:
        return Frustrated()
    elif poweron:
        return controlPower()
    elif shutdown:
        return controlShutDown()
    
    else:
        return "Whaaat?"  

def moodHappy():
	#w = wave.open("C:/Users/nisha/Downloads/Avicii.mp3","r")
	print("Hooray, Lets celebrate!")
	time.sleep(2)
	print("Playing 'If you are happy and you know it'")
	mixer.init()
	mixer.music.load('C:/Users/nisha/Downloads/Happy.mp3')
	mixer.music.play()
	time.sleep(23)
		
def moodSad():
	print("Dont you worry!")
	time.sleep(3)
	print("Avicii is always with us in our hearts with his fantastic music :)")
	time.sleep(4)
	print("Okay, Let me search a song for you")
	time.sleep(1)
	print("Playing 'Without you by Avicii'")
	mixer.init()
	mixer.music.load('C:/Users/nisha/Downloads/Avicii.mp3')
	mixer.music.play()
	time.sleep(55)
				
def Frustrated():
	print("Okay, Even I feel the same, Let us get frustated together!")
	time.sleep(2)
	mixer.init()
	mixer.music.load('C:/Users/nisha/Downloads/wonder_woman_theme.mp3')
	mixer.music.play()
	time.sleep(23)
    
def controlPower():
    print("Okay, Let me think")
    time.sleep(1)
    payload = {
        "method":"setPowerStatus",
        "id":55,
        "params":[
         {
          "status":"active"
          }],
        "version":"1.1"

    }
    respons = requests.post(url1, data=json.dumps(payload), headers=headers).json()
    print(respons)
    
def controlShutDown():
	print("Okay, Let me think")
	time.sleep(1)
	payload = {
        "method":"setPowerStatus",
        "id":55,
        "params":[
         {
          "status":"off"
         }],
        "version":"1.1"
    }
	respons = requests.post(url1, data=json.dumps(payload), headers=headers).json()
	print(respons)
	
	
def controlVolumeMute():
# Example echo method
	print("Okay, Let me think")
	time.sleep(1)
	payload = {
        "method":"setAudioMute",
        "id":601,
        "params":[
         {
          "mute":"on"
         }],
        "version":"1.1"
    }
	respons = requests.post(url, data=json.dumps(payload), headers=headers).json()
	print(respons)
   
    
def controlVolumeMuteOff():
# Example echo method
    print("UnMuted")
    payload = {
        "method":"setAudioMute",
        "id":601,
        "params":[
         {
          "mute":"off"
         }],
        "version":"1.1"
    }
    respons = requests.post(url, data=json.dumps(payload), headers=headers).json()
    	

client = Wit(access_token= "KXHAFEIGLTH7TNZ2IG4IGM3J32J6O65X")
text =  RecognizeSpeech('myspeech.wav', 5)
print("\nYou said: {}".format(text))

#client.message(text)
resp = None
with open('myspeech.wav', 'rb') as f:
  resp = client.speech(f, None, {'Content-Type': 'audio/wav'})
print(str(handle_message(resp)))