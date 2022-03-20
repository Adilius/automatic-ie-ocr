import app.preprocessing as preprocessing
import app.text_detection as text_detection
import app.text_recognition as text_recognition
import app.util as util
import cv2

# Input image
#input_image = cv2.imread("form_filled\\top_form\\1.png", cv2.IMREAD_COLOR)
input_image = cv2.imread("form_blank\\top_form\\blank.png", cv2.IMREAD_COLOR)
util.show_image(input_image)

# ______ Preprocess ______
preprocessed_image = preprocessing.preprocess_image(
    image=input_image, grayscale=True, noise_removal=True, deskew=False
)
util.show_image(preprocessed_image)

# ______ Text detection ______
# Create 3-layer image to fit text detection
merged_image = cv2.merge([preprocessed_image, preprocessed_image, preprocessed_image])

image_boxes, bounding_boxes_coordinates = text_detection.detect_text(
    merged_image, dimensions=True, threshold=0.1, overlap_threshold=0.01
)
# util.show_image(image_boxes)


# ______  Text recognition ______
text = text_recognition.recognize_text(preprocessed_image, bounding_boxes_coordinates)
# print(text)
