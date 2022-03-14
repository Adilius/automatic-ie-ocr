import cv2
import numpy as np
import util
import imutils.object_detection as imutils
import csv
from operator import itemgetter


NEW_DIMENSIONS = 32

def get_new_dimensions(image):

    print('Calculating new dimensions to fit model')

    # Get new image shape
    try:
        height, width = image.shape
    except ValueError:
        height, width, _ = image.shape
    
    new_height = (height//NEW_DIMENSIONS)*NEW_DIMENSIONS    # EAST model requires image size multiples of 32
    new_width = (width//NEW_DIMENSIONS)*NEW_DIMENSIONS
    
    # Get ratio change
    h_ratio = height/new_height
    w_ratio = width/new_width

    #print("Old dimensions",height, width)
    #print("New dimensions",new_height, new_width)
    #print("Ratio change", h_ratio, w_ratio)

    return new_height, new_width, h_ratio, w_ratio

def text_prediction(image, new_height, new_width):

    print("Running text detection neural network")

    # Load the frozen EAST model
    model = cv2.dnn.readNet('..\models\\frozen_east_text_detection.pb')

    # Create a 4D input blob, (123.68, 116.78, 103.94) ImageNet
    blob = cv2.dnn.blobFromImage(image, 1, (new_width, new_height),(123.68, 116.78, 103.94), True, False)

    # Pass the blob to network
    model.setInput(blob)

    # Get output layers
    output_layers = model.getUnconnectedOutLayersNames()

    # Text detection prediction
    (geometry, scores) = model.forward(output_layers)
    return geometry, scores

def thresholding(geometry, scores, threshold):

    print("Thresholding low score boxes")

    rectangles = list()
    confidence_score = list()
    for i in range(geometry.shape[2]):
        for j in range(geometry.shape[3]):

            # If score for bounding box falls below threshold
            if scores[0][0][i][j] < threshold:
                continue

            bottom_x = int(j*4 + geometry[0][1][i][j])
            bottom_y = int(i*4 + geometry[0][2][i][j])


            top_x = int(j*4 - geometry[0][3][i][j])
            top_y = int(i*4 - geometry[0][0][i][j])

            rectangles.append((top_x, top_y, bottom_x, bottom_y))
            confidence_score.append(float(scores[0][0][i][j]))

    return rectangles, confidence_score

# use Non-max suppression to get the required rectangles
def non_max_suppression(rectangles, confidence_score, overlap_threshold):

    print('Removing overlaps with non-maximum suppression')

    fin_boxes = imutils.non_max_suppression(np.array(rectangles), probs=confidence_score, overlapThresh=overlap_threshold)
    return fin_boxes

def draw_rectangles(image, rectangles, h_ratio, w_ratio):

    print('Drawing rectangles on image')

    image_copy = image.copy()

    for (x1, y1, x2, y2) in rectangles:

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)


        cv2.rectangle(image_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return image_copy

def detect_text(image, dimensions: bool = True, threshold: float = 0.1, overlap_threshold: float = 0.5):

    print('___ TEXT DETECTION ____')

    if dimensions:
        new_height, new_width, h_ratio, w_ratio = get_new_dimensions(image)
    else:
        new_height, new_width, _ = image.shape
        h_ratio, w_ratio = 1,1
        print("Dimensions kept change", new_height, new_width)

    geometry, scores = text_prediction(image, new_height, new_width)

    rectangles, confidence_score = thresholding(geometry, scores, threshold)

    final_boxes = non_max_suppression(rectangles, confidence_score, overlap_threshold)

    adjusted_boxes = readjust_boxes(final_boxes, h_ratio, w_ratio)

    image_copy = draw_rectangles(image, adjusted_boxes, h_ratio, w_ratio)

    return image_copy, adjusted_boxes

def readjust_boxes(boxes, h_ratio, w_ratio):
    for index, box in enumerate(boxes):
        boxes[index] = [int(box[0]*w_ratio), int(box[1]*h_ratio), int(box[2]*w_ratio), int(box[3]*h_ratio)]

    boxes = sorted(boxes, key=itemgetter(1))

    return boxes
        

if __name__ == "__main__":

    # Load input preprocessed image
    print('Reading preprocessed image')
    image = cv2.imread("..\output_images\preprocessed.png", cv2.IMREAD_COLOR)
    #util.show_image(image)

    # Text detection
    print('Running text detection')
    image_copy, final_boxes = detect_text(image, dimensions=True, threshold = 0.1, overlap_threshold = 0.5)

    # Show result
    print('Saving image and bounding boxes')
    #util.show_image(image_copy)
    util.write_image('..\output_images\\text_detection.png',image_copy)

    # Save text detected bounding boxes coordinates
    with open("..\output_csv\\text_detection_boxes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(final_boxes)