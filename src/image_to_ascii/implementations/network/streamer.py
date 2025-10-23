""" import socket as sk
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
    host="20.20.23.199"
    print(f"Websocket started \n...listening on {host}:{port}")
    async with ws.serve(main,host,port):
        await asyncio.Future()  
    
    

def modify(image:np.ndarray)->np.ndarray:
    image=cvt_scale_np(image,Filter.AVERAGE)
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



 """

import asyncio
import json
import time
import cv2 as cv
import numpy as np
import websockets
from collections import deque

HOST, PORT = "0.0.0.0", 5555
WIDTH, CHAR_ASPECT = 250, 2.0
ASCII_CHARS = "@%#*+=-:. "
FPS, DIFF_T, FLOW_T = 30, 12, 1.0

clients, lock = set(), asyncio.Lock()

def to_gray(frame):
    h, w = frame.shape[:2]
    target_h = int((WIDTH * h / w) / CHAR_ASPECT)
    g = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    return cv.resize(g, (WIDTH, target_h), interpolation=cv.INTER_AREA)

def to_ascii(gray):
    idx = np.rint((gray / 255) * (len(ASCII_CHARS) - 1)).astype(int)
    return np.array(list(ASCII_CHARS))[idx]

async def broadcast(msg):
    if not clients: return
    async with lock:
        await asyncio.gather(*[c.send(msg) for c in clients], return_exceptions=True)

async def producer():
    cap = cv.VideoCapture(0)
    prev_small, prev_grid = None, None
    hist = deque(maxlen=2)
    lk = dict(winSize=(15,15), maxLevel=2,
              criteria=(cv.TERM_CRITERIA_EPS|cv.TERM_CRITERIA_COUNT,10,0.03))
    while True:
        t0 = time.time()
        ok, frame = cap.read()
        if not ok: continue
        frame = cv.flip(frame, 1)
        small, grid = to_gray(frame), to_ascii(to_gray(frame))
        if prev_small is None:
            await broadcast(json.dumps({"type":"full","frame":"\n".join("".join(r) for r in grid)}))
            prev_small, prev_grid = small.copy(), grid.copy()
            continue
        diff = cv.absdiff(small, prev_small)
        h, w = small.shape
        step = max(4, w//20)
        p0 = np.array([[x,y] for y in range(0,h,step) for x in range(0,w,step)], np.float32).reshape(-1,1,2)
        p1, st, _ = cv.calcOpticalFlowPyrLK(prev_small, small, p0, None, **lk)
        flow = np.zeros_like(small, np.float32)
        for (a,b,ok_) in zip(p0.reshape(-1,2), p1.reshape(-1,2), st.reshape(-1)):
            if ok_:
                dx,dy = b-a
                if 0<=int(b[0])<w and 0<=int(b[1])<h:
                    flow[int(b[1]),int(b[0])] = max(flow[int(b[1]),int(b[0])], (dx*dx+dy*dy)**0.5)
        flow = cv.GaussianBlur(flow,(7,7),0)
        motion = (diff>DIFF_T)|(flow>FLOW_T)
        changed=[]
        for r in range(grid.shape[0]):
            if np.any(grid[r]!=prev_grid[r]) and np.any(motion[r]):
                changed.append((r,"".join(grid[r])))
        if changed:
            await broadcast(json.dumps({"type":"patch","changes":[{"row":r,"line":l} for r,l in changed]}))
        hist.append(grid.copy())
        prev_small, prev_grid = small.copy(), grid.copy()
        await asyncio.sleep(max(0,1/FPS-(time.time()-t0)))

async def handler(ws):
    clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        clients.remove(ws)

async def run_server():
    async with websockets.serve(handler,HOST,PORT):
        print(f"Streaming ASCII video on ws://{HOST}:{PORT}")
        await producer()

if __name__=="__main__":
    asyncio.run(run_server())
