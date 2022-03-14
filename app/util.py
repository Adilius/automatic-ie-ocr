import cv2
import matplotlib.pyplot as plt

def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)

def write_image(image_name, image):
    cv2.imwrite(image_name, image)

def show_image_plt(image):
    plt.imshow(image)
    plt.show()