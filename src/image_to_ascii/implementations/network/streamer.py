import socket as sk
import pickle as pk
import cv2 as cv
import numpy as np
from image_to_ascii.implementations.base_converter import convert_image_to_ascii
from image_to_ascii.implementations.mode_converter import cvt_scale_np
from image_to_ascii.implementations.method import Filter

from PIL import Image as ImageSrc
from PIL.Image import Image
import asyncio
import websockets as ws




    

async def initStream():
    port=5555
    host="0.0.0.0"
    print(f"Websocket started \n...listening on {host}:{port}")
    async with ws.serve(main,host,port):
        await asyncio.Future()  
    
    

def modify(image:np.ndarray)->np.ndarray:
    image=cvt_scale_np(image,Filter.LUMINANCE)
    ascii_frame = convert_image_to_ascii(image,200)
    return ascii_frame



async def main(socket):
    instance = cv.VideoCapture(0)
    try:
        while True:
            isFrame,frame=instance.read()
            if isFrame:
                frame=cv.flip(frame,1)
                frame=modify(frame)
                await stream(frame,socket)
            if cv.waitKey(1) and ord("q") == 0xFF:
                break
    except KeyboardInterrupt:
        instance.release()
        cleanup()


async def stream(frame:str,sk):
    await sk.send(str(frame))
    await asyncio.sleep(1/30)
    #self.client.sendall(frame.encode())


def cleanup():
    print("\nCleaning UP")
    cv.destroyAllWindows()

    


if __name__ == "__main__":
    asyncio.run(initStream())
