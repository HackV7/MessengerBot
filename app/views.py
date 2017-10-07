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

    elif message_text == 'airline_checkin':
        response_msg = airline_checkin(fbid)    

    elif message_text == 'airline_itinerary':
        response_msg = airline_itinerary(fbid)    

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


                    if message_text == 'bpass':
                        post_facebook_message(sender_id,'boarding_pass_template')

                    elif message_text == 'cpass':
                        post_facebook_message(sender_id,'airline_checkin')

                    elif message_text == 'ipass':
                        post_facebook_message(sender_id,'airline_itinerary')


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
                                    "logo_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Vistara_logo.svg/250px-Vistara_logo.svg.png",
                                    "header_image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Vistara_logo.svg/250px-Vistara_logo.svg.png",
                                    "qr_code": "M1SMITH\/NICOLAS  CG4X7U nawouehgawgnapwi3jfa0wfh",
                                    "above_bar_code_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/UPC-A-036000291452.png/440px-UPC-A-036000291452.png",
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



def airline_checkin(fbid):
    response_object = {
                          "recipient": {
                            "id": fbid
                          },
                          "message": {
                            "attachment": {
                              "type": "template",
                              "payload": {
                                "template_type": "airline_checkin",
                                "intro_message": "Check-in is available now.",
                                "locale": "en_US",        
                                "pnr_number": "ABCDEF",
                                        "checkin_url": "https://www.airvistara.com/trip/traveller-info",  
                                "flight_info": [
                                  {
                                    "flight_number": "f001",
                                    "departure_airport": {
                                      "airport_code": "SFO",
                                      "city": "San Francisco",
                                      "terminal": "T4",
                                      "gate": "G8"
                                    },
                                    "arrival_airport": {
                                      "airport_code": "SEA",
                                      "city": "Seattle",
                                      "terminal": "T4",
                                      "gate": "G8"
                                    },
                                    "flight_schedule": {
                                      "boarding_time": "2016-01-05T15:05",
                                      "departure_time": "2016-01-05T15:45",
                                      "arrival_time": "2016-01-05T17:30"
                                    }
                                  }
                                ]
                              }
                            }
                          }
                        }

    return json.dumps(response_object)




def airline_itinerary(fbid):
    response_object = {
                          "recipient": {
                            "id": fbid
                          },
                          "message": {
                            "attachment": {
                              "type": "template",
                              "payload": {
                                "template_type": "airline_itinerary",
                                "intro_message": "Here is your flight itinerary.",
                                "locale": "en_US",
                                "pnr_number": "ABCDEF",
                                "passenger_info": [
                                  {
                                    "name": "Farbound Smith Jr",
                                    "ticket_number": "0741234567890",
                                    "passenger_id": "p001"
                                  },
                                  {
                                    "name": "Nick Jones",
                                    "ticket_number": "0741234567891",
                                    "passenger_id": "p002"
                                  }
                                ],
                                "flight_info": [
                                  {
                                    "connection_id": "c001",
                                    "segment_id": "s001",
                                    "flight_number": "KL9123",
                                    "aircraft_type": "Boeing 737",
                                    "departure_airport": {
                                      "airport_code": "SFO",
                                      "city": "San Francisco",
                                      "terminal": "T4",
                                      "gate": "G8"
                                    },
                                    "arrival_airport": {
                                      "airport_code": "SLC",
                                      "city": "Salt Lake City",
                                      "terminal": "T4",
                                      "gate": "G8"
                                    },
                                    "flight_schedule": {
                                      "departure_time": "2016-01-02T19:45",
                                      "arrival_time": "2016-01-02T21:20"
                                    },
                                    "travel_class": "business"
                                  },
                                  {
                                    "connection_id": "c002",
                                    "segment_id": "s002",
                                    "flight_number": "KL321",
                                    "aircraft_type": "Boeing 747-200",
                                    "travel_class": "business",
                                    "departure_airport": {
                                      "airport_code": "SLC",
                                      "city": "Salt Lake City",
                                      "terminal": "T1",
                                      "gate": "G33"
                                    },
                                    "arrival_airport": {
                                      "airport_code": "AMS",
                                      "city": "Amsterdam",
                                      "terminal": "T1",
                                      "gate": "G33"
                                    },
                                    "flight_schedule": {
                                      "departure_time": "2016-01-02T22:45",
                                      "arrival_time": "2016-01-03T17:20"
                                    }
                                  }
                                ],
                                "passenger_segment_info": [
                                  {
                                    "segment_id": "s001",
                                    "passenger_id": "p001",
                                    "seat": "12A",
                                    "seat_type": "Business"
                                  },
                                  {
                                    "segment_id": "s001",
                                    "passenger_id": "p002",
                                    "seat": "12B",
                                    "seat_type": "Business"
                                  },
                                  {
                                    "segment_id": "s002",
                                    "passenger_id": "p001",
                                    "seat": "73A",
                                    "seat_type": "World Business",
                                    "product_info": [
                                      {
                                        "title": "Lounge",
                                        "value": "Complimentary lounge access"
                                      },
                                      {
                                        "title": "Baggage",
                                        "value": "1 extra bag 50lbs"
                                      }
                                    ]
                                  },
                                  {
                                    "segment_id": "s002",
                                    "passenger_id": "p002",
                                    "seat": "73B",
                                    "seat_type": "World Business",
                                    "product_info": [
                                      {
                                        "title": "Lounge",
                                        "value": "Complimentary lounge access"
                                      },
                                      {
                                        "title": "Baggage",
                                        "value": "1 extra bag 50lbs"
                                      }
                                    ]
                                  }
                                ],
                                "price_info": [
                                  {
                                    "title": "Fuel surcharge",
                                    "amount": "1597",
                                    "currency": "USD"
                                  }
                                ],
                                "base_price": "12206",
                                "tax": "200",
                                "total_price": "14003",
                                "currency": "USD"
                              }
                            }
                          }
                        }

    return json.dumps(response_object)





