import math
import json
import pprint
import csv
import difflib

# Factor to beat the average distance to be in cluster
DISTANCE_CONSTANT = 0.9


def group_fields(boxes: dict):

    print(f"Clustering boxes...")

    # pprint.pprint(boxes)

    total_distance = 0

    # CALCULATING DISTANCES
    for origin_id, origin_box in boxes.items():
        shortest_path = list()

        # Get origin box position
        origin_box_pos = (
            int(origin_box["positions"]["midpoint"]["x"]),
            int(origin_box["positions"]["midpoint"]["y"]),
        )

        # iterate over all neighbors
        for neighbor_id, neighbor_box in boxes.items():

            # Don't iterate over origin box
            if neighbor_id != origin_id:

                # Get neighbor boxes position
                neighbor_box_pos = (
                    int(neighbor_box["positions"]["midpoint"]["x"]),
                    int(neighbor_box["positions"]["midpoint"]["y"]),
                )

                # Calculate distance between origin and neighbor
                weighted_eucledian_distance = math.sqrt(
                    pow((origin_box_pos[0] - neighbor_box_pos[0]) / 2, 2)
                    + pow((origin_box_pos[1] - neighbor_box_pos[1]), 2)
                )

                shortest_path.append(weighted_eucledian_distance)

        shortest_path.sort()
        shortest_path = shortest_path[:1]
        total_distance += shortest_path[0]

    # GET AVERAGE DISTANCE
    avg_distance = total_distance / len(boxes)
    print(f"Average cluster distance : {avg_distance}")

    # ASSIGN CLUSTER
    for origin_id, origin_box in boxes.items():

        # Get origin box position
        origin_box_pos = (
            int(origin_box["positions"]["midpoint"]["x"]),
            int(origin_box["positions"]["midpoint"]["y"]),
        )

        # Iterate over all neighbors
        for neighbor_id, neighbor_box in boxes.items():

            # Don't iterate over origin box
            if neighbor_id != origin_id:

                # get neighbor pos
                neighbor_box_pos = (
                    int(neighbor_box["positions"]["midpoint"]["x"]),
                    int(neighbor_box["positions"]["midpoint"]["y"]),
                )

                # Calculate distance between origin and neighbor
                weighted_eucledian_distance = math.sqrt(
                    pow((origin_box_pos[0] - neighbor_box_pos[0]) / 2, 2)
                    + pow((origin_box_pos[1] - neighbor_box_pos[1]), 2)
                )

                # Assign neighbor new cluster ID
                if weighted_eucledian_distance <= avg_distance * 0.9:
                    boxes[str(neighbor_id)]["cluster"] = boxes[str(origin_id)][
                        "cluster"
                    ]

    clustered_boxes = list()
    for _, _ in boxes.items():
        clustered_boxes.append(list())
    for id, box in boxes.items():
        clustered_boxes[box["cluster"]].append(box["text"].lstrip())
    clustered_boxes = [x for x in clustered_boxes if x != []]

    print(clustered_boxes)
    #pprint.pprint(boxes, sort_dicts=False)
    return clustered_boxes, boxes

def assign_question_boxes(boxes: dict, grouped_boxes: list):
    print("Detecting questions in filled form...")

    # For each word in each cluster
    for cluster_id, cluster in enumerate(grouped_boxes):
        for word in cluster:
            
            # Get remaining words from image
            remaining_words_list = list()
            for id, box in boxes.items():
                if box["question"] == False:
                    remaining_words_list.append(box["text"])

            # Match word to remaining words
            match = fuzzy_compare(word, remaining_words_list)

            # Assign box the question flag and assign cluster ID
            for id, box in boxes.items():
                if box["text"] == match and box["question"] == False:
                    box["question"] = True
                    box["cluster"] = cluster_id
                    #print("match")
            #print(word, match)
            #print(remaining_words_list)
    #pprint.pprint(boxes, sort_dicts=False)
    return boxes

def cluster_questions(assigned_boxes: dict):
    print("Clustering answers")

    # ASSIGN CLUSTER TO ANSWER BOXES
    for question_id, question_box in assigned_boxes.items():

        is_question = question_box["question"]
        if is_question:
            for neighbor_id, neighbor_box in assigned_boxes.items():
                is_question = neighbor_box["question"]
                if is_question:                
                    if neighbor_id != question_id:

                        question_cluster = question_box["cluster"]
                        neighbor_cluster = neighbor_box["cluster"]

                        if question_cluster == neighbor_cluster:
                            #print(f'{question_id=} {neighbor_id=}')

                            # Modify first box
                            assigned_boxes[question_id]["text"] = assigned_boxes[question_id]["text"] + " " + assigned_boxes[neighbor_id]["text"]
                            assigned_boxes[question_id]["positions"]["bottom_right"] = assigned_boxes[neighbor_id]["positions"]["bottom_right"]

                            question_x = assigned_boxes[question_id]["positions"]["midpoint"]["x"]
                            neighbor_x = assigned_boxes[neighbor_id]["positions"]["midpoint"]["x"]
                            new_x = int((neighbor_x + question_x)/2)
                            assigned_boxes[question_id]["positions"]["midpoint"]["x"] = new_x

                            question_y = assigned_boxes[question_id]["positions"]["midpoint"]["y"]
                            neighbor_y = assigned_boxes[neighbor_id]["positions"]["midpoint"]["y"]
                            new_y = int((neighbor_y + question_y)/2)
                            assigned_boxes[question_id]["positions"]["midpoint"]["y"] = new_y

                            # Remove second box
                            assigned_boxes.pop(neighbor_id)

                            # Assign new clusters
                            assigned_boxes = cluster_questions(assigned_boxes)
                            return assigned_boxes
                            
    #pprint.pprint(assigned_boxes, sort_dicts=False)
    return assigned_boxes



def cluster_answers(assigned_boxes: dict):
    print("Clustering answers...")

    shortest_path = list()
    
    # ASSIGN ANSWERS TO CLUSTERS
    for answer_id, answer_box in assigned_boxes.items():

        is_question = answer_box["question"]
        if not is_question:

            # Get answer box position
            answer_box = (
                int(answer_box["positions"]["midpoint"]["x"]),
                int(answer_box["positions"]["midpoint"]["y"]),
            )

            # Iterate over all question clusters
            for question_id, question_box in assigned_boxes.items():


                is_question = question_box["question"]
                if is_question:

                    # Get neighbor boxes position
                    neighbor_box_pos = (
                            int(question_box["positions"]["midpoint"]["x"]),
                            int(question_box["positions"]["midpoint"]["y"]),
                        )

                        # Calculate distance between origin and neighbor
                    weighted_eucledian_distance = math.sqrt(
                            pow((answer_box[0] - neighbor_box_pos[0])/2, 2)
                            + pow((answer_box[1] - neighbor_box_pos[1])*2, 2)
                        )

                    shortest_path.append((weighted_eucledian_distance, question_id, answer_id))

            shortest_path = sorted(shortest_path, key=lambda tup: tup[0])
            shortest_path = shortest_path[:1]
            #print(shortest_path)
            q_id = int(shortest_path[0][1])
            a_id = int(shortest_path[0][2])
            #print(f'{q_id=} {a_id=}')
            assigned_boxes[str(a_id)]["cluster"] = assigned_boxes[str(q_id)]["cluster"]
            shortest_path.clear()

    #pprint.pprint(assigned_boxes, sort_dicts=False)
    return assigned_boxes

def save_clustered_answers(clustered_answers: dict):

    print('Saving to CSV...')

    questions_list = list()
    answers_list = list()

    for id, box in clustered_answers.items():
        if box["question"] is True:
            questions_list.append([])
            questions_list[int(box["cluster"])].append(box["text"])

    questions_list = [item for sublist in questions_list for item in sublist]

    for id, box in clustered_answers.items():
        if box["question"] is False:
            answers_list.append('')
            answers_list[int(box["cluster"])] = answers_list[int(box["cluster"])]  +  box["text"] + ' '

    answers_list = [x.rstrip() for x in answers_list]
    answers_list = [x for x in answers_list if x != []]
    answers_list = [x for x in answers_list if x != '']

    print(questions_list)
    print(answers_list)

    with open('output_csv\\output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(questions_list, answers_list))
    

def fuzzy_compare(origin_word: str, words: list):
    match = difflib.get_close_matches(word=origin_word, possibilities=words, n=1)[0]
    return match


def save_grouped_fields(grouped_fields: list):
    print("Saving fields to CSV")

    # Save text detected bounding boxes coordinates
    with open("output_csv\\grouped_fields.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(grouped_fields)


# To help easier manipulate boxes
def convert_to_dict(boxes: list):
    boxes_dict = dict()

    for index, box in enumerate(boxes):
        boxes_dict[str(index)] = {}
        boxes_dict[str(index)]["positions"] = dict()
        boxes_dict[str(index)]["positions"]["top_left"] = dict()
        boxes_dict[str(index)]["positions"]["top_left"]["x"] = box[0]
        boxes_dict[str(index)]["positions"]["top_left"]["y"] = box[1]

        boxes_dict[str(index)]["positions"]["bottom_right"] = dict()
        boxes_dict[str(index)]["positions"]["bottom_right"]["x"] = box[2]
        boxes_dict[str(index)]["positions"]["bottom_right"]["y"] = box[3]

        boxes_dict[str(index)]["positions"]["midpoint"] = dict()
        boxes_dict[str(index)]["positions"]["midpoint"]["x"] = box[4]
        boxes_dict[str(index)]["positions"]["midpoint"]["y"] = box[5]

        boxes_dict[str(index)]["question"] = False
        boxes_dict[str(index)]["text"] = box[-1]
        boxes_dict[str(index)]["cluster"] = index

    # pprint.pprint(boxes_dict, sort_dicts=False)
    return boxes_dict


def post_process_blank(boxes: list):

    print("___ POST-PROCESS BLANK ___")
    boxes_dict = convert_to_dict(boxes)

    grouped_boxes, _ = group_fields(boxes_dict)

    save_grouped_fields(grouped_boxes)

    return grouped_boxes

def post_process_filled(boxes: list, grouped_boxes: list):
    print("___ POST-PROCESS FILLED ___")
    boxes_dict = convert_to_dict(boxes)

    assigned_boxes = assign_question_boxes(boxes_dict, grouped_boxes)

    clustered_questions =  cluster_questions(assigned_boxes)

    clustered_answers = cluster_answers(clustered_questions)

    save_clustered_answers(clustered_answers)

    pass
