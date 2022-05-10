import app.preprocessing as preprocessing
import app.text_detection as text_detection
import app.text_recognition as text_recognition
import app.post_proccess as post_process
import app.util as util
import cv2


def blank_clustering(file_name: str):
    # Input image
    # input_image = cv2.imread("form_filled\\top_form\\1.png", cv2.IMREAD_COLOR)
    input_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    #util.show_image(input_image)

    # ______ Preprocess ____________
    preprocessed_image = preprocessing.preprocess_image(
        image=input_image, grayscale=True, noise_removal=True, deskew=False
    )
    #util.show_image(preprocessed_image)
    # ______________________________

    # ______ Text detection ________
    # Create 3-layer image to fit text detection

    merged_image = cv2.merge(
        [preprocessed_image, preprocessed_image, preprocessed_image]
    )

    text_detected_image, boxes = text_detection.detect_text(
        merged_image, threshold=0.1, overlap_threshold=0.01
    )
    # util.show_image(image_boxes)
    # ______________________________

    # ______  Text recognition ______
    boxes = text_recognition.recognize_text(preprocessed_image, boxes)
    # _______________________________

    # ________ Post-process ________
    grouped_boxes = post_process.post_process_blank(boxes)
    # _______________________________

    return grouped_boxes


def information_extraction(file_name: str, grouped_boxes: list):
    input_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    #util.show_image(input_image)
    # ______ Preprocess ____________
    preprocessed_image = preprocessing.preprocess_image(
        image=input_image, grayscale=True, noise_removal=True, deskew=False
    )
    #util.show_image(preprocessed_image)
    # ______ Text detection ________
    merged_image = cv2.merge(
        [preprocessed_image, preprocessed_image, preprocessed_image]
    )
    text_detected_image, boxes = text_detection.detect_text(
        merged_image, threshold=0.1, overlap_threshold=0.01
    )
    #util.show_image(text_detected_image)
    # ______  Text recognition ______
    boxes = text_recognition.recognize_text(preprocessed_image, boxes)
    # ________ Post-process ________
    clustered_image = post_process.post_process_filled(boxes, grouped_boxes, merged_image)
    util.show_image(clustered_image)


if __name__ == "__main__":
    print("_________ BLANK CLUSTERING __________")
    grouped_boxes = blank_clustering("form_blank\\bottom_form\\blank.png")
    print("_____________________________________")
    print("\n" + "\n" + "\n" + "\n")

    print("_________ INFORMATION EXTRACTION __________")
    information_extraction(
        "form_filled\\bottom_form\\1.png", grouped_boxes
    )
    print("___________________________________________")
