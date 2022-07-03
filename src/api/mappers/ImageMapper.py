import cv2
import numpy as np
from PIL import Image


class ImageMapper:

    @staticmethod
    def from_api(file):
        image = Image.open(file.stream)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image

    @staticmethod
    def from_image(image):
        pass
