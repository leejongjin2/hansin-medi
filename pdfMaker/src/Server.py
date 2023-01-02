import asyncio
import websockets
import webbrowser
from DB import get_data

class SingletonServer(object):
        
    def start_server(cls):
        url = "/home/hwi/github/hansin-medi/pdfMaker/src/result.html"
        webbrowser.open(url)
        asyncio.get_event_loop().run_forever() 
    
    async def accept(websocket, path):
        data = await websocket.recv()    
        print("receive : " + data)
        user_info = get_data()
        await websocket.send(user_info)
        data = await websocket.recv()
        if data =="close":
            print('Close Server Loop')
            asyncio.get_event_loop().stop()
            
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonServer, cls).__new__(cls)
            server = websockets.serve(cls.accept, "localhost", 8888)
            asyncio.get_event_loop().run_until_complete(server)
            print('Start New Server')
            return cls.instance
        else:
            print('Recycle Server')
            return cls.instance