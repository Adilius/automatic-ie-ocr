import math
import json
import pprint


def group_fields(boxes: dict):

    #pprint.pprint(boxes)

    total_distance = 0
    avg_distance = 0

    for id, box in boxes.items():
        shortest_path = list()
        pprint.pprint(box)

        box_pos = (int(box["positions"]["midpoint"]["x"]), int(box["positions"]["midpoint"]["y"]))
        print(box_pos)

    # For each box
    for index, box in enumerate(boxes):

        box_pos = (box[4], box[5])

        # For each neighbor
        for neighbor in [x for i, x in enumerate(boxes) if i != index]:

            neighbor_pos = (neighbor[4], neighbor[5])

            weighted_eucledian_distance = math.sqrt(
                pow((box_pos[0] - neighbor_pos[0])/2, 2) + pow((box_pos[1] - neighbor_pos[1]), 2))

            shortest_path.append(weighted_eucledian_distance)

            print(
                f'Index: {index}  Box: {box[-1]} {box_pos}  Neighbor: {neighbor[-1]} {neighbor_pos}  Distance: {weighted_eucledian_distance}')

        shortest_path.sort()
        shortest_path = shortest_path[:1]
        total_distance += shortest_path[0]
        
    
    avg_distance = total_distance/len(boxes)
    print(f'{avg_distance=}')

    # For each box
    for index, box in enumerate(boxes):

        box_pos = (box[4], box[5])

        shortest_path = list()

        # For each neighbor
        for neighbor in [x for i, x in enumerate(boxes) if i != index]:

            neighbor_pos = (neighbor[4], neighbor[5])

            weighted_eucledian_distance = math.sqrt(
                pow((box_pos[0] - neighbor_pos[0])/2, 2) + pow((box_pos[1] - neighbor_pos[1]), 2))

            if weighted_eucledian_distance <= avg_distance:
                print(
                    f'Index: {index}  Box: {box[-1]} {box_pos}  Neighbor: {neighbor[-1]} {neighbor_pos}  Distance: {weighted_eucledian_distance}')


def fuzzy_compare(blank_words: list, recognized_words: list):
    pass

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

        boxes_dict[str(index)]["frame"] = True
        boxes_dict[str(index)]["text"] = box[-1]
        boxes_dict[str(index)]["cluster"] = -1
        
    #pprint.pprint(boxes_dict, sort_dicts=False)
    return boxes_dict
    

def post_process(boxes: list):

    

    print('___ POST-PROCESS ___')
    boxes_dict = convert_to_dict(boxes)

    group_fields(boxes_dict)
