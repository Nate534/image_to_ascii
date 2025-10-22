import socket as sk
import pickle as pk
import cv2 as cv
import numpy as np
from image_to_ascii.implementations.base_converter import convert_image_to_ascii
from PIL import Image as ImageSrc
from PIL.Image import Image


class Stream:
    def __init__(self):
        self.socket = sk.socket(sk.AF_INET,sk.SOCK_DGRAM)
        self.initStream()
        self.stream()

    def initStream(self):
        self.socket.bind(("0.0.0.0",8080))
        print(":: Streaming Socket 0.0.0.0:8080")
        
    def modify(self,image:np.ndarray)->np.ndarray:
        print(image)
        return image



    def stream(self):
        self.instance = cv.VideoCapture(0)
        try:
            while True:
                isFrame,frame=self.instance.read()
                if isFrame:
                    frame=cv.flip(frame,1)
                    frame=self.modify(frame)
                    cv.imshow("this is me",frame)
                if cv.waitKey(1) and ord("q") == 0xFF:
                    break
        except KeyboardInterrupt:
            self.cleanup()


    def cleanup(self):
        print("\nCleaning UP")
        self.instance.release()
        self.socket.close()
        cv.destroyAllWindows()

        


if __name__ == "__main__":
    Stream()



