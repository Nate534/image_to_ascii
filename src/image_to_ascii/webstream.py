import websockets
import io
import cv2
import PIL.Image as Image
import asyncio

class WebStreamer:
    def __init__(self):
        pass


    def server(self,socket):
        pass

    async def main(self):
        async with websockets.serve(self.server,"0.0.0.0",5555):
            print("WebSocket server running on ws://localhost:8765")
            await asyncio.Future()    

if __name__=="__main__":
    streamer=WebStreamer()  
    asyncio.run(streamer.main())