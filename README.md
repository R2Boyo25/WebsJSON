Library for adding handlers for messages over a websocket.

messages are formatted like:
```json
{
  "type":"type",
  "key1":"data1",
  "key2":"data2",
  ...
}
```

`asyncio` needs to be imported before using the library

make an instance of `WSHandler`:
```py
WSHandlerInstance = WebsJSON.WSHandler("ws://ip:port") # any arguments given to this are passed to websockets.connect, except onConnect and printJSONDecodeError
```

make a handler with:
```py
@WSHandlerInstance.handle("type")
async def typeHandler(ctx, **kwargs):
```
or a default handler with:
```py
@WSHandlerInstance.handle()
async def defaultHandler(ctx, **kwargs):
```

ctx will be a tuple:
```py
(websocket, Message)
``` 

and then you connect with
```py
asyncio.run(WSHandlerInstance.connect())
```
