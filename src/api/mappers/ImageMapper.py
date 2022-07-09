from io import BytesIO

import cv2
import numpy as np
from PIL import Image


class ImageMapper:

    @staticmethod
    def from_api(file):
        """
        Maps an Image from buffer to opencv-Image
        :param file: File as Buffer
        :return: opencv-Image (Numpy Array)
        """
        image = Image.open(file.stream)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image

    @staticmethod
    def from_image(image):
        """
        Maps an opencv-Image to buffer
        :param image: opencv-Image (Numpy Array)
        :return: File as Buffer
        """
        is_success, buffer = cv2.imencode(".png", image)
        return BytesIO(buffer)
