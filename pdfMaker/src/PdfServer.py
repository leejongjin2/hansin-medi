import asyncio
import websockets
import webbrowser

async def accept(websocket, path):
    data = await websocket.recv()    
    print("receive : " + data)
    await websocket.send("To Be JsonData")
    data = await websocket.recv()
    if data =="close":
        print('close')
        asyncio.get_event_loop().stop()

def start_server():
    global server

    url = "/home/hwi/github/hansin-medi/pdfMaker/src/result.html"
    webbrowser.open(url)
    asyncio.get_event_loop().run_forever() 
    
# 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다. 
global server
server = websockets.serve(accept, "localhost", 8899)
asyncio.get_event_loop().run_until_complete(server)
    