class Context:
    def __init__(self, websocket, message):
        self.websocket = websocket
        self.message = message
    
    def __getitem__(self, item):
        return [self.websocket, self.message][item]
        
    def send(self, *args, **kwargs):
        self.websocket.send(*args, **kwargs)