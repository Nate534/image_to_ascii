import cv2 as cv
import numpy as np
import asyncio
import websockets as ws
from image_to_ascii.implementations.base_converter import convert_image_to_ascii
from image_to_ascii.implementations.mode_converter import cvt_scale_np
from image_to_ascii.implementations.method import Filter

prev_frame = None

lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)
)

DIFF_T = 10
FLOW_T = 1.0
STEP = 4


async def initStream():
    host = "0.0.0.0"
    port = 5555
    async with ws.serve(main, host, port):
        await asyncio.Future()


def modify(image):
    gray = cvt_scale_np(image, Filter.LUMINANCE)
    ascii_frame = convert_image_to_ascii(gray, 200)
    return ascii_frame, gray


async def main(socket):
    global prev_frame
    cap = cv.VideoCapture(0)

    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        frame = cv.flip(frame, 1)

        ascii_frame, frame = modify(frame)
        send_frame = False

        if prev_frame is None:
            send_frame = True
        else:
            diff = cv.absdiff(frame, prev_frame)
            h, w = frame.shape

            p0 = np.array(
                [[x, y] for y in range(0, h, STEP) for x in range(0, w, STEP)],
                np.float32
            ).reshape(-1, 1, 2)

            p1, st, _ = cv.calcOpticalFlowPyrLK(prev_frame, frame, p0, None, **lk_params)

            flow = np.zeros_like(frame, np.float32)

            for a, b, ok_ in zip(p0.reshape(-1, 2), p1.reshape(-1, 2), st.reshape(-1)):
                if ok_:
                    dx, dy = b - a
                    x, y = int(b[0]), int(b[1])
                    if 0 <= x < w and 0 <= y < h:
                        flow[y, x] = max(flow[y, x], (dx ** 2 + dy ** 2) ** 0.5)

            motion = (diff > DIFF_T) | (flow > FLOW_T)

            if np.any(motion):
                send_frame = True

        if send_frame:
            await stream(ascii_frame, socket)

        prev_frame = frame.copy()

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


async def stream(frame, socket):
    await socket.send(str(frame))
    await asyncio.sleep(1 / 30)


if __name__ == "__main__":
    asyncio.run(initStream())
