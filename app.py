import app.preprocessing as preprocessing
import app.text_detection as text_detection
import app.text_recognition as text_recognition
import app.post_proccess as post_process
import app.util as util
import cv2
import os
import pathlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# High = Less boxes
TEXT_DETECTION_THRESHOLD = 0.5

# Low = Less overlap
TEXT_OVERLAP_THRESHOLD = 0.1


def ocr_engine(input_image):

    # ______ Preprocess ____________
    preprocessed_image = preprocessing.preprocess_image(
        image=input_image, grayscale=True, noise_removal=True, deskew=False
    )
    # util.show_image(preprocessed_image)
    # ______________________________

    # ______ Text detection ________
    # Create 3-layer image to fit text detection

    merged_image = cv2.merge(
        [preprocessed_image, preprocessed_image, preprocessed_image]
    )
    text_detected_image, boxes = text_detection.detect_text(
        merged_image,
        threshold=TEXT_DETECTION_THRESHOLD,
        overlap_threshold=TEXT_OVERLAP_THRESHOLD,
    )
    # plt.imshow(text_detected_image)
    # plt.show()
    # util.show_image(text_detected_image)
    # ______________________________

    # ______  Text recognition ______
    boxes = text_recognition.recognize_text(preprocessed_image, boxes)
    # _______________________________

    return boxes


def blank_clustering(file_name: str):

    # ______ INPUT IMAGE ____________
    input_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    # util.show_image(input_image)
    # _______________________________

    boxes = ocr_engine(input_image)

    # ________ Post-process ________
    grouped_boxes = post_process.post_process_blank(boxes)
    # _______________________________

    return grouped_boxes


def information_extraction(file_name: str, grouped_boxes: list):

    # ______ INPUT IMAGE ____________
    input_image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    # util.show_image(input_image)
    # _______________________________

    boxes = ocr_engine(input_image)

    # ________ Post-process ________
    clustered_image, output_list = post_process.post_process_filled(
        boxes, grouped_boxes, input_image
    )
    # util.show_image(clustered_image)
    return clustered_image, output_list
    # _______________________________


if __name__ == "__main__":

    PATH = str(pathlib.Path(__file__).parent.resolve())
    FOLDER_NAMES = []
    for (dirpath, dirnames, filenames) in os.walk(PATH + "\\input\\form_blank\\"):
        FOLDER_NAMES.extend(dirnames)
        break
    # print(FOLDER_NAMES)

    for folder in FOLDER_NAMES:
        print("_________ BLANK CLUSTERING __________")
        grouped_boxes = blank_clustering("input\\form_blank\\" + folder + "\\blank.png")
        print("_____________________________________")
        print("\n" + "\n" + "\n" + "\n")

        for (dirpath, dirnames, filenames) in os.walk(
            PATH + "\\input\\form_filled\\" + folder + "\\"
        ):
            for file in filenames:
                full_file_path = PATH + "\\input\\form_filled\\" + folder + "\\" + file
                # print(full_file_path)
                print("_________ INFORMATION EXTRACTION __________")
                print(f"File: {full_file_path}")
                image, output_list = information_extraction(
                    full_file_path, grouped_boxes
                )
                util.write_image(PATH + "\\output\\" + folder + "\\" + file, image)
                util.save_csv(
                    PATH + "\\output\\" + folder + "\\" + file[:-3] + "csv", output_list
                )
                print("___________________________________________")
