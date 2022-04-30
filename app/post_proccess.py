import math
import json
import pprint

# Factor to beat the average distance to be in cluster
DISTANCE_CONSTANT = 0.9

def group_fields(boxes: dict):

    print(f'Clustering boxes...')

    #pprint.pprint(boxes)

    total_distance = 0

    # CALCULATING DISTANCES
    for origin_id, origin_box in boxes.items():
        shortest_path = list()

        # Get origin box position
        origin_box_pos = (int(origin_box["positions"]["midpoint"]["x"]), int(
            origin_box["positions"]["midpoint"]["y"]))

        # iterate over all neighbors
        for neighbor_id, neighbor_box in boxes.items():

            # Don't iterate over origin box
            if neighbor_id != origin_id:

                # Get neighbor boxes position
                neighbor_box_pos = (int(neighbor_box["positions"]["midpoint"]["x"]), int(
                    neighbor_box["positions"]["midpoint"]["y"]))

                # Calculate distance between origin and neighbor
                weighted_eucledian_distance = math.sqrt(
                    pow((origin_box_pos[0] - neighbor_box_pos[0])/2, 2) + pow((origin_box_pos[1] - neighbor_box_pos[1]), 2))

                shortest_path.append(weighted_eucledian_distance)

        shortest_path.sort()
        shortest_path = shortest_path[:1]
        total_distance += shortest_path[0]

    # GET AVERAGE DISTANCE
    avg_distance = total_distance/len(boxes)
    print(f'Average cluster distance : {avg_distance}')

    # ASSIGN CLUSTER
    for origin_id, origin_box in boxes.items():
        
        # Get origin box position
        origin_box_pos = (int(origin_box["positions"]["midpoint"]["x"]), int(
            origin_box["positions"]["midpoint"]["y"]))

        # Iterate over all neighbors
        for neighbor_id, neighbor_box in boxes.items():

            # Don't iterate over origin box
            if neighbor_id != origin_id:

                # get neighbor pos
                neighbor_box_pos = (int(neighbor_box["positions"]["midpoint"]["x"]), int(
                    neighbor_box["positions"]["midpoint"]["y"]))

                # Calculate distance between origin and neighbor
                weighted_eucledian_distance = math.sqrt(
                    pow((origin_box_pos[0] - neighbor_box_pos[0])/2, 2) + pow((origin_box_pos[1] - neighbor_box_pos[1]), 2))

                # Assign neighbor new cluster ID
                if weighted_eucledian_distance <= avg_distance*0.9:
                    boxes[str(neighbor_id)]["cluster"] = boxes[str(origin_id)]["cluster"]

    clustered_boxes = list()
    for _, _ in boxes.items():
        clustered_boxes.append('')
    for id, box in boxes.items():
        clustered_boxes[box['cluster']] = (clustered_boxes[box['cluster']] + ' ' + box['text']).lstrip()
    clustered_boxes = [x for x in clustered_boxes if x != '']

    print(clustered_boxes)
    pprint.pprint(boxes)
    return boxes

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
        boxes_dict[str(index)]["cluster"] = index

    #pprint.pprint(boxes_dict, sort_dicts=False)
    return boxes_dict


def post_process_blank(boxes: list):

    print('___ POST-PROCESS BLANK ___')
    boxes_dict = convert_to_dict(boxes)

    grouped_boxes = group_fields(boxes_dict)
