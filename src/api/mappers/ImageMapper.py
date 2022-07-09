from io import BytesIO
from zipfile import ZipFile

import cv2
import numpy as np
from PIL import Image


class ImageMapper:

    @staticmethod
    def from_api(file):
        """
        Maps an Image from buffer to opencv-Image
        :param file: File as Buffer
        :return: opencv-image (Numpy Array)
        """
        image = Image.open(file.stream)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image

    @staticmethod
    def from_image(image):
        """
        Maps an opencv-image to buffer
        :param image: opencv-image (Numpy Array)
        :return: File as Buffer
        """
        is_success, buffer = cv2.imencode(".png", image)
        return BytesIO(buffer)

    @staticmethod
    def from_images(images):
        """
        Maps multiple opencv-images to zip file as buffer
        :param images: list of opencv-images
        :return: Zip file as buffer
        """
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for i, image in enumerate(images):
                is_success, buffer = cv2.imencode(".png", image)
                zf.writestr(f'sudoku_solution_{i}.png', buffer)
        stream.seek(0)
        return stream
