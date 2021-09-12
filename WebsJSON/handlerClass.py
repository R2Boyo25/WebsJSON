import websockets
import json
import asyncio
from .messageClass import Message

class EmptyArgumentsException(Exception):
    pass

class WSHandler():
    def __init__(self, *args, **kwargs):
        self.kwargs = {}
        self.printJsonDecodeError = True
        self.onConnect = None

        for key, value in kwargs.items():
            if key.lower() == 'printjsondecodeerror':
                self.printJsonDecodeError = value
            elif key.lower() == 'onconnect':
                self.onConnect = value
            else:
                self.kwargs[key] = value

        self.args = args
        self.handlers = {}

        if len(args) == 0:
            raise EmptyArgumentsException()            

    def handel(self, typename):
        def decorator_handel(function = '_default'):
            self.handlers[typename] = function
        return decorator_handel
        
    def handle(self, typename = '_default'):
        def decorator_handle(function):
            self.handlers[typename] = function
        return decorator_handle

    async def connect(self):
        async with websockets.connect(*self.args, **self.kwargs) as ws:
            if self.onConnect:
                await self.onConnect(ws)
            async for message in ws:
                try:
                    message = Message(message)
                    args = {}
                    for item in message.toDict().items():
                        if item[0] != 'type':
                            args[item[0]] = item[1]
                    if message.type in self.handlers.keys():
                        await self.handlers[message.type]((ws, message), **args)
                    else:
                        if '_default' in self.handlers.keys():
                            await self.handlers['_default']((ws, message), **args)
                except json.JSONDecodeError as exception:
                    if self.printJsonDecodeError:
                        print('JSONDecodeError on\n{}'.format(json.dumps(message, indent = 4)))
