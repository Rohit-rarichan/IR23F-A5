import time 
import socket
from ds_protocol import *


class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
    self.token = None
    self.dsuserver = dsuserver #"168.235.86.101"
    self.username = username
    self.password = password
    self.client = None

		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      self.client = connect_to_server(self.dsuserver)
      timestamp = get_timestamp()
      if self.username and self.password:
        join_msg = join(self.username, self.password)
        self.client.send(join_msg.encode('utf-8'))
        resp = self.client.recv(1024).decode()
        response_json = json.loads(resp)
        if response_json['response']['type'] == 'ok':
          self.token = response_json['response']['token']
          send_to_recipient = direct_message(self.token, message, recipient, timestamp)
          self.client.send(send_to_recipient.encode('utf-8'))
          response1 = self.client.recv(1024).decode()
          print(response1)
          return True
    except Exception as e:
      print(f"Error retrieving new messages: {e}")
		
  def retrieve_new(self) -> list:
    try:
      if self.token:
        send_message = "new"
        reading_msgs = msgs_response(self.token, send_message)
        self.client.send(reading_msgs.encode('utf-8'))
        response2 = self.client.recv(1024).decode()
        retrieved_unread_list = server_response(response2)
        return retrieved_unread_list
    except Exception as e:
      print(f"Error retrieving new messages: {e}")
        # must return a list of DirectMessage objects containing all new messages
  
  def retrieve_all(self) -> list:
    try:
      if self.token:
        send_message = "all"
        reading_msgs = msgs_response(self.token, send_message)
        self.client.send(reading_msgs.encode('utf-8'))
        response2 = self.client.recv(1024).decode()
        retrieved_all_list = server_response(response2)
        return retrieved_all_list
    except Exception as e:
      print(f"Error retrieving all messages: {e}")
    # must return a list of DirectMessage objects containing all messages
  
def connect_to_server(server):
    port = "3021"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, int(port)))
    print(f"client connected to {server} on {port}")
    return client


def get_timestamp():
   return str(time.time())