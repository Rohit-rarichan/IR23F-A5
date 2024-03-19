import json
from pathlib import *

class DsuFileError(Exception):
    pass

class Profile:
    def __init__(self, username = None, password = None, dsuserver = None):
        self.username = username 
        self.password = password 
        self.dsuserver = dsuserver
        self.friends = []
        self.messages = [] 

    def add_friend(self, username):
        if username not in self.friends:
            self.friends.append(username)
    
    def add_message(self, message):
        self.messages.append(message)

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    

