from typing import final
import cv2
import numpy as np
import util
import csv

ALPHABET_SET = "0123456789abcdefghijklmnopqrstuvwxyz"
BLANK = '-'
CHAR_SET = BLANK + ALPHABET_SET

# Read input file for bounding boxes coordinates
def read_bounding_boxes(filename: str):

    # Store each coordinates
    bounding_boxes_coordinates = list()

    # Read and convert each row into a list of integers
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            bounding_boxes_coordinates.append([int(n) for n in row])
    
    return bounding_boxes_coordinates

# Returns most likely text
def most_likely(scores):
    text = ""
    for i in range(scores.shape[0]):
        c = np.argmax(scores[i][0])
        text += CHAR_SET[c]
    return text

# Remove blanks and duplicates
def map_rule(text):

    # Resulting text
    char_list = []

    # Check first character if its not blank
    if text[0] != '-':
        char_list.append(text[0])

    # Check the rest of characters
    for i in range(1,len(text),1):
        if text[i] != '-':
            if text[i] != text[i-1]:
                char_list.append(text[i])

    # Join all characters into a string
    return ''.join(char_list)

def recognize_text(image, bounding_boxes_coordinates: list):

    print('___ TEXT RECOGNITION ___')

    # Load model
    model = cv2.dnn.readNet('..\models\crnn.onnx')

    # List to contain outputed text
    output_text = list()

    # Iterate over each segment
    for box in bounding_boxes_coordinates:


        # Segment image containing one text box
        image_segment = image[box[1]:box[3]+1, box[0]:box[2]+1]

        # Create blob
        blob = cv2.dnn.blobFromImage(image_segment, scalefactor=1/127.5, size=(100,32), mean=127.5)

        # Pass blob to network
        model.setInput(blob)

        # Recognize characters and produce scores
        scores = model.forward()

        # Extract character from highest score
        predicted_text = most_likely(scores)

        # Mapping rule
        final_text = map_rule(predicted_text)

        print(f'Recognizing: {final_text}               ', end="\r")

        #print(final_text)
        output_text.append(final_text)

    print(f'Recognized {len(output_text)} words!          ')
    return output_text

if __name__ == "__main__":

    # Read in the processed image
    image = cv2.imread('..\output_images\preprocessed.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Read bounding boxes
    bounding_boxes_coordinates = read_bounding_boxes('..\output_csv\\text_detection_boxes.csv')

    # Text recognition
    text = recognize_text(image, bounding_boxes_coordinates)

    # Print result
    #print(text)

    for i in range(len(text)):
        bounding_boxes_coordinates[i].append(text[i])

    # Save bounding box coordinates with recognized text
    with open("..\output_csv\\recognized_text.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(bounding_boxes_coordinates)
