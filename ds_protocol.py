# ds_protocol.py

# Rohit George Rarichan
# rraricha@uci.edu
# 36126645

import json
from collections import namedtuple


# Namedtuple to hold the values retrieved from json messages.

DataTuple = namedtuple('DataTuple', ['foo','baz'])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)

def join(username:str, password: str):
    join_msg = {"join":{"username": username, "password": password, "token": ''}}
    return json.dumps(join_msg)

def post(message:str, user_token:str, timestamp:str ):
   post_msg = {"token": user_token, "post":{"entry":message, "timestamp": timestamp}}  #or use time.time()
   return json.dumps(post_msg)

def bio_send(bio:str, user_token:str, timestamp:str):
   bio_msg = {"token": user_token, "post":{"entry":bio, "timestamp": timestamp}}
   return json.dumps(bio_msg)

def direct_message(user_token: str, message: str, recipient: str, timestamp: str):
   direct_msg = {"token" : user_token, "directmessage" : {"entry" : message, "recipient" : recipient, "timestamp" : timestamp}}
   return json.dumps(direct_msg)

def msgs_response(user_token : str, send_message: str):
   resp_msg = {"token" : user_token, "directmessage" : send_message}
   return json.dumps(resp_msg)
   
def server_response(response_send_message): #processing the response from the msgs_response function 
   response = json.loads(response_send_message)
   if "response" in response:
      response_type = response["response"]["type"]
      if response_type == "ok":
         if "messages" in response["response"]:
            return response["response"]["message"]
         else:
            return response["response"]["message"]
      else:
         return response["response"]["error"]
   else:
      return "Invalid Format"


   