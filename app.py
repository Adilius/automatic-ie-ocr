import app.preprocessing as preprocessing
import app.text_detection as text_detection
import app.text_recognition as text_recognition
import app.post_proccess as post_process
import app.util as util
import cv2

# Input image
#input_image = cv2.imread("form_filled\\top_form\\1.png", cv2.IMREAD_COLOR)
input_image = cv2.imread("form_blank\\top_form\\blank.png", cv2.IMREAD_COLOR)
util.show_image(input_image)


# ______ Preprocess ____________    
preprocessed_image = preprocessing.preprocess_image(
    image=input_image, grayscale=True, noise_removal=True, deskew=False
)
util.show_image(preprocessed_image)
# ______________________________


# ______ Text detection ________
# Create 3-layer image to fit text detection
merged_image = cv2.merge([preprocessed_image, preprocessed_image, preprocessed_image])

text_detected_image, boxes = text_detection.detect_text(
    merged_image, threshold=0.1, overlap_threshold=0.01
)
# util.show_image(image_boxes)
# ______________________________


# ______  Text recognition ______
boxes = text_recognition.recognize_text(preprocessed_image, boxes)
# _______________________________

# ________ Post-process ________
post_process.post_process(boxes)
# _______________________________
