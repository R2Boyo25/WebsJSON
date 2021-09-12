import json

class Message:
    def __init__(self, message:any):
        if type(message) != dict:
            self.message = json.loads(message)
        else:
            self.message = message
    
    def __getitem__(self, item:any) -> any:
        return self.message[item]
        
    def __getatrr__(self, item:str) -> any:
        return self.message[item]

    def __setitem__(self, name:any, value:any) -> None:
        self.message[name] = value
    
    #def __setattr__(self, name:str, value:any) -> None:
    #    self.message[name] = value

    @property
    def type(self):
        return self.message['type']

    def __delitem__(self, name:str) -> None:
        del self.message[name]

    def __delattr__(self, name:any) -> None:
        del self.message[name]

    def pop(self, name: any) -> any:
        return self.message.pop(name)

    def __str__(self) -> str:
        return json.dumps(self.message)
    
    def toDict(self) -> dict:
        return self.message