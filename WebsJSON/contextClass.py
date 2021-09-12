class Context:
    def __init__(self, websocket, message):
        self.websocket = websocket
        self.message = message
    
    def __getitem__(self, item):
        if item == 0:
            return self.websocket
        elif item == 1:
            return self.message
        else:
            raise IndexError
        
    def send(self, *args, **kwargs):
        self.websocket.send(*args, **kwargs)