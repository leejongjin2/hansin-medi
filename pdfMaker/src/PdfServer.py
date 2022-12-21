import os
import asyncio
import websockets
import webbrowser
        
# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    # while True:
    # 클라이언트로부터 메시지를 대기한다.
    data = await websocket.recv()
    
    print("receive : " + data)
    # 클라인언트로 echo를 붙여서 재 전송한다.
    await websocket.send("To Be JsonData")

def start_server():
    url = "/home/hwi/github/hansin-medi/pdfMaker/src/result.html"
    webbrowser.open(url)
    # 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다. 
    server = websockets.serve(accept, "localhost", 8899)
    # 비동기로 서버를 대기한다.
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever() 