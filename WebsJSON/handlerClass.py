import websockets
import json
import asyncio
import threading
from .messageClass import Message
from .contextClass import Context

class EmptyArgumentsException(Exception):
    pass

class WSHandler():
    def __init__(self, *args, **kwargs):
        self.kwargs = {}
        self.printJsonDecodeError = True
        self.onConnect = None
        self.thread = None
        self.sleeptime = 0.2
        self.ws = None

        for key, value in kwargs.items():
            if key.lower() == 'printjsondecodeerror':
                self.printJsonDecodeError = value
            elif key.lower() == 'onconnect':
                self.onConnect = value
            elif key.lower() == 'thread':
                self.thread = value
            elif key.lower() == 'sleep':
                self.sleeptime = value
            elif key.lower() == 'ws' or key.lower() == 'websocket':
                self.ws = value
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

    async def _connect(self, ws = None):
        if not self.ws:
            ws = await websockets.connect(*self.args, **self.kwargs)
        else:
            if not ws:
                ws = self.ws
        #async with websockets.connect(*self.args, **self.kwargs) as ws:
        try:
            if self.onConnect:
                await self.onConnect(ws)
            #if self.thread:
            #    self.startThread(self.thread, ws)
            asyncio.to_thread(self.recvMessages, ws)
            await self.thread
        except KeyboardInterrupt:
            await ws.close()
        
    def connect(self, ws = None, eloop= None):
        if eloop:
            pass
        else:
            asyncio.run(self._connect(ws))
    
    def startThread(self, function, ws):
        thread = threading.Thread(target=self.asyncioThread, args=(function, self, ws))

        thread.start()
    
    def asyncioThread(self, function, *args):
        asyncio.run(function(*args))
    
    async def recvMessages(self, websocket):
        async for message in ws:
            if self.thread:
                await asyncio.sleep(self.sleeptime)
            try:
                message = Message(message)
                args = {}
                for item in message.toDict().items():
                    if item[0] != 'type':
                        args[item[0]] = item[1]
                if message.type in self.handlers.keys():
                    await self.handlers[message.type](Context(ws, message), **args)
                else:
                    if '_default' in self.handlers.keys():
                        await self.handlers['_default'](Context(ws, message), **args)
            except json.JSONDecodeError as exception:
                if self.printJsonDecodeError:
                    print('JSONDecodeError on\n{}'.format(json.dumps(message, indent = 4)))
