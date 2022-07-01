import logging
import math
import sys

import cv2
import numpy as np

log = logging.getLogger(__name__)


class GridGameScanner:

    @staticmethod
    def detect_lines(image, threshold1=20, threshold2=100):
        dst = cv2.Canny(image, threshold1, threshold2, None, 3)
        lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
        return lines

    @staticmethod
    def add_border_to_image(image, border_size, color=None):
        if color is None:
            color = [255, 255, 255]

        bordersize = border_size
        image = cv2.copyMakeBorder(
            image,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=color
        )
        return image

    @staticmethod
    def find_biggest_contour(image, threshold1=20, threshold2=100):
        dst = cv2.Canny(image, threshold1, threshold2, None, 3)
        contours, hierarchy = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        return sorted_contours[0]  # largest item

    @staticmethod
    def get_corners_of_contour(contour):
        # Find smallest rectangle which includes the contour
        rect = cv2.minAreaRect(contour)
        box = np.int0(cv2.boxPoints(rect))

        # Find corners using the euclidean distance
        corners = []
        for reference_point in box:
            corner = []
            corner_distance = sys.maxsize
            for point in contour:
                distance = np.linalg.norm(reference_point - point[0])
                if distance < corner_distance:
                    corner = point
                    corner_distance = distance
            corners.append(corner)
        corners = np.array(corners)
        corners = GridGameScanner.sort_corners(corners)
        return corners

    @staticmethod
    def sort_corners(pts):
        """
        Sorts corners in order top left, top right, bottom left, bottom right
        """
        x_sorted = pts[np.argsort(pts[:, 0, 0]), :]
        leftMost = x_sorted[:2, :]
        rightMost = x_sorted[2:, :]
        tl, bl = leftMost[np.argsort(leftMost[:, 0, 1]), :]
        tr, br = rightMost[np.argsort(rightMost[:, 0, 1]), :]

        return np.stack([tl, tr, bl, br])

    @staticmethod
    def perspective_transform(img, to_pts, from_pts=None):
        width = len(img[0])
        height = len(img)

        if from_pts is None:
            from_pts = np.array([[0, 0], [width, 0], [0, height], [width, height]], np.float32)

        matrix = cv2.getPerspectiveTransform(to_pts, from_pts)
        warped = cv2.warpPerspective(img, matrix, (width, height))
        return warped

    @staticmethod
    def merge_lines(lines, rho_threshold=10, theta_threshold=0.2):
        new_lines = []
        lines = lines.tolist()
        while len(lines) > 0:
            rho = lines[0][0][0]
            theta = lines[0][0][1]

            tmp_lines = [lines[0]]
            for j in range(1, len(lines)):
                rho_j = lines[j][0][0]
                theta_j = lines[j][0][1]
                if rho + rho_threshold > rho_j > rho - rho_threshold \
                        and theta + theta_threshold > theta_j > theta - theta_threshold:
                    tmp_lines.append(lines[j])

            avg_rho = sum([line[0][0] for line in tmp_lines]) / len(tmp_lines)
            avg_theta = sum([line[0][1] for line in tmp_lines]) / len(tmp_lines)
            new_lines.append([[avg_rho, avg_theta]])

            for line in tmp_lines:
                lines.remove(line)
        return np.array(new_lines)

    @staticmethod
    def get_row_and_col_indexes(lines):
        rows = []
        cols = []
        threshold1 = math.radians(45)
        threshold2 = math.radians(135)
        threshold3 = math.radians(225)
        threshold4 = math.radians(315)
        for line in lines:
            if line[0][1] > threshold4:
                cols.append(line[0][0])
            elif line[0][1] > threshold3:
                rows.append(-line)
            elif line[0][1] > threshold2:
                cols.append(-line[0][0])
            elif line[0][1] > threshold1:
                rows.append(line[0][0])
            else:
                cols.append(line[0][0])

        # Combine to one np.array
        cols = np.stack(cols, axis=0)
        rows = np.stack(rows, axis=0)

        # Sort ascending
        cols = np.sort(cols)
        rows = np.sort(rows)

        return rows, cols

    @staticmethod
    def split_image_into_tiles(lines, min_tile_size=20, padding=3):
        rows, cols = GridGameScanner.get_row_and_col_indexes(lines)
        tiles = []
        last_row = int(rows[0])
        for i in range(1, len(rows)):
            start_row, end_row = last_row, int(rows[i])
            if end_row - start_row < min_tile_size:  # Skip if too small
                continue

            last_col = int(cols[0])
            for j in range(1, len(cols)):
                start_col, end_col = last_col, int(cols[j])
                if end_col - start_col < min_tile_size:
                    continue

                tile = {
                    'row_start': start_row + padding,
                    'row_end': end_row - padding,
                    'col_start': start_col + padding,
                    'col_end': end_col - padding
                }
                tiles.append(tile)
                last_col = int(cols[j])
            last_row = int(rows[i])
        return tiles

    def scan(self, image):
        log.debug('Looking for the largest contour')
        image = self.add_border_to_image(image, 10)
        largest_item = self.find_biggest_contour(image)

        log.debug('Searching corners of contour')
        corners = self.get_corners_of_contour(largest_item)

        log.debug('Perform perspective transformation')
        warped = self.perspective_transform(image, corners.astype(np.float32))

        log.debug('Search for lines')
        lines = self.detect_lines(warped)
        lines = self.merge_lines(lines, rho_threshold=20, theta_threshold=0.5)
        log.info(f'{len(lines)} lines detected')

        log.debug('Split image into tiles')
        padding = len(warped) // 100
        tiles = self.split_image_into_tiles(lines, padding=padding)

        return warped, tiles
