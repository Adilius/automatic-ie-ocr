import cv2
import csv
import numpy as np
import util

# Scale font scale to text box width
def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 60, 1)):
        textSize = cv2.getTextSize(text, fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            return scale/10

# Read input file for bounding boxes coordinates
def read_recognized_text(filename: str):

    # Store each coordinates
    boxes = list()

    # Read and convert each row into a list of integers
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            coordinates = [int(n) for n in row[:-1]]
            text = row[-1:]
            line = coordinates + text
            boxes.append(line)

    return boxes

def restruct(image_template: str, recognized_text_boxes: str):

    print('___ RESTRUCTURING ___')

    # Read in the image size
    image = cv2.imread(image_template, cv2.IMREAD_COLOR)
    height, width = image.shape[:2]

    # Create blank image
    blank_image = np.zeros((height, width, 3), np.uint8)
    blank_image[:,:] = (255,255,255)

    # Read in box coordinates and text
    boxes = read_recognized_text(recognized_text_boxes)

    for box in boxes:

        print(f'Writing: {box[-1]}               ', end="\r", flush=True)

        scale = get_optimal_font_scale(box[-1], box[2]-box[0])

        cv2.putText(img=blank_image,
        text=box[-1],
        org=(box[0], box[1]),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=scale,
        color=(0,0,0),
        thickness=1)

    print(f'Written {len(boxes)} words!          ')

    return blank_image

if __name__ == '__main__':
    restructed_image = restruct('..\image.png', '..\output_csv\\recognized_text.csv')

    util.write_image('..\output_images\\restructured_image.png',restructed_image)
    util.show_image(restructed_image)
