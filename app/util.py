import cv2
import matplotlib.pyplot as plt


def show_image(image):
    image = resize(image, width=1200)
    cv2.imshow("image", image)
    cv2.waitKey(0)


def write_image(image_name, image):
    cv2.imwrite(image_name, image)


def show_image_plt(image):
    plt.imshow(image)
    plt.show()


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
