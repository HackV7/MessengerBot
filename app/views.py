#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import requests

# Create your views here.

VERIFY_TOKEN = 'VHack7'
PAGE_ACCESS_TOKEN = 'EAABuZBXsi6owBAI8wPGGASZA0tKJZC9eZAU3RKwaSiuiV5YNHVZCfggOHfrZAoXAiOsD8ZBWaTA4fC1FHsRYj7ZAl4n2DTzvCDzNFKlQ5w5ToisrMUYyDt2MvFp72edE8VYSHBEMf08kYsjZCZCOheAgVg5m4cCIY4MmDh6n7DYji2mqWNJzG73PKB'


def userdeatils(fbid):
    url = 'https://graph.facebook.com/v2.6/' + fbid + '?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=' + PAGE_ACCESS_TOKEN
    resp = requests.get(url=url)
    data =json.loads(resp.text)
    return data



def post_facebook_message(fbid,message_text):
    
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN

    if message_text == 'boarding_pass_template':
        response_msg = boarding_pass_template(fbid)

    else:
        response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})

    requests.post(post_message_url, 
                    headers={"Content-Type": "application/json"},
                    data=response_msg)



class MyChatBotView(generic.View):
	def get(self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))
		print (incoming_message)

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print (message)
				try:
					sender_id = message['sender']['id']
                    message_text = message['message']['text']
                    DataInstance = userdeatils(sender_id)
                    firstName = '%s'%(DataInstance['first_name'])
                    userInstance = UserData.objects.get_or_create(Fbid =sender_id)[0]


					if message_text == 'bpass':
						post_facebook_message(sender_id,'boarding_pass_template')
						
					else:
						sender_id = message['sender']['id']
						message_text = message['message']['text']
						post_facebook_message(sender_id,message_text) 

				except Exception as e:
					print (e)
					pass

		return HttpResponse()  

def index(request):
	return HttpResponse('Hello world')


def boarding_pass_template(fbid):
    
    response_object = {
						  "recipient": {
						    "id": fbid
						  },
						  "message": {
						    "attachment": {
						      "type": "template",
						      "payload": {
						        "template_type": "airline_boardingpass",
						        "intro_message": "You are checked in.",
						        "locale": "en_US",
						        "boarding_pass": [
						          {
						            "passenger_name": "SMITH\/NICOLAS",
						            "pnr_number": "CG4X7U",
						            "seat": "74J",            
						            "logo_image_url": "https:\/\/www.example.com\/en\/logo.png",
						            "header_image_url": "https:\/\/www.example.com\/en\/fb\/header.png",
						            "qr_code": "M1SMITH\/NICOLAS  CG4X7U nawouehgawgnapwi3jfa0wfh",
						            "above_bar_code_image_url": "https:\/\/www.example.com\/en\/PLAT.png",
						            "auxiliary_fields": [
						              {
						                "label": "Terminal",
						                "value": "T1"
						              },
						              {
						                "label": "Departure",
						                "value": "30OCT 19:05"
						              }
						            ],
						            "secondary_fields": [
						              {
						                "label": "Boarding",
						                "value": "18:30"
						              },
						              {
						                "label": "Gate",
						                "value": "D57"
						              },
						              {
						                "label": "Seat",
						                "value": "74J"
						              },
						              {
						                "label": "Sec.Nr.",
						                "value": "003"
						              }
						            ],
						            "flight_info": {
						              "flight_number": "KL0642",
						              "departure_airport": {
						                "airport_code": "JFK",
						                "city": "New York",
						                "terminal": "T1",
						                "gate": "D57"
						              },
						              "arrival_airport": {
						                "airport_code": "AMS",
						                "city": "Amsterdam"
						              },
						              "flight_schedule": {
						                "departure_time": "2016-01-02T19:05",
						                "arrival_time": "2016-01-05T17:30"
						              }
						            }
						          }
						        ]
						      }
						    }
						  }
						}

    return json.dumps(response_object)











