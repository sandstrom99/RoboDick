
import cv2 as cv
import numpy as np

with open("./img/avatar.png", "rb") as f:
    image_bytes = f.read()
    decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    print(decoded)
