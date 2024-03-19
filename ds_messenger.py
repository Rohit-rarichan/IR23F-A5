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
    self.dsuserver = "168.235.86.101"
    self.username = None
    self.password = None
    self.client = None

		
  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      self.client = connect_to_server(self.dsuserver)
      timestamp = get_timestamp()
      username = input("Enter your username: ")
      password = input("Enter the password: ")
      join_msg = join(username, password)
      self.client.send(join_msg.encode('utf-8'))
      resp = self.client.recv(1024).decode()
      response_json = json.loads(resp)
      if response_json['response']['type'] == 'ok':
        self.token = response_json['response']['token']
        send_to_recipient = direct_message(self.token, message, recipient, timestamp)
        self.client.send(send_to_recipient.encode('utf-8'))
        response1 = self.client.recv(1024).decode()
        print(response1)


    except:
      pass
		
  def retrieve_new(self) -> list:
    send_message = "new"
    reading_msgs = msgs_response(self.token, send_message)
    self.client.send(reading_msgs.encode('utf-8'))
    response2 = self.client.recv(1024).decode()
    retrieved_unread_list = server_response(response2)
    for i in retrieved_unread_list:
      print(i["message"])
    # must return a list of DirectMessage objects containing all new messages
 
  def retrieve_all(self) -> list:
    send_message = "all"
    reading_msgs = msgs_response(self.token, send_message)
    self.client.send(reading_msgs.encode('utf-8'))
    response2 = self.client.recv(1024).decode()
    retrieved_all_list = server_response(response2)
    for i in retrieved_all_list:
      print(i["message"])
    # must return a list of DirectMessage objects containing all messages
    pass
  
def connect_to_server(server):
    port = "3021"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server, int(port)))
    print(f"client connected to {server} on {port}")
    return client


def get_timestamp():
   return str(time.time())