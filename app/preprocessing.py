import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import util

def min_max(image):
    image_min = np.min(image)
    image_max = np.max(image)
    new_image = (image - image_min) / (image_max - image_min)
    return new_image


def grayscale_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_image(image):
    return cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)


def noise_remove(image):
    # blur
    blur = cv2.GaussianBlur(image, (0, 0), sigmaX=33, sigmaY=33)

    # divide
    divide = cv2.divide(image, blur, scale=255)

    # otsu threshold
    thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh


def deskew_image(image):
    # detect box
    image = cv2.convertScaleAbs(image)
    thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # find angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # deskew
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    image = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return image


def preprocess_image(
    image, grayscale: bool, noise_removal: bool, deskew: bool
):

    print('___ PREPROCESSING ____')

    # Turn image to gray
    print('Grayscale: ', end="")
    if grayscale:
        print('True')
        image = grayscale_image(image)
    else:
        print('False')

    # Remove noise gaussian
    print('Gaussian noise removal: ', end="")
    if noise_removal:
        print('True')
        image = noise_remove(image)
        image = cv2.convertScaleAbs(image)
    else:
        print('False')

    # Rotate image
    print('Deskew: ', end="")
    if deskew:
        print('True')
        image = deskew_image(image)
    else:
        print('False')

    return image


if __name__ == "__main__":

    # Input image
    print('Reading input image...')
    image = cv2.imread("..\image.png", cv2.IMREAD_COLOR)
    util.show_image(image)

    # Preprocess
    print('Preprocessing image...')
    image = preprocess_image(
        image=image, grayscale=True, noise_removal=True, deskew=True
    )

    # Showing & saving result image
    print('Saving image...')
    util.show_image(image)
    util.write_image('..\output_images\preprocessed.png', image)
