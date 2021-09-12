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

`asyncio` needs to be imported before using the library
