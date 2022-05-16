import cv2
import matplotlib.pyplot as plt
import csv


def show_image(image):
    image = resize(image, width=900)
    cv2.imshow("image", image)
    cv2.waitKey(0)


def write_image(path, image):
    cv2.imwrite(path, image)

def save_csv(path: str, data: list):
    print(data)
    with open(path, 'w') as f:
        csv_writer = csv.writer(f)
        for row in data:
            csv_writer.writerow(row)

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
