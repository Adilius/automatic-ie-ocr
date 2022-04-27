import math


def group_fields(boxes: list):
    print(boxes)

    for index, box in enumerate(boxes):

        box_pos = (box[4], box[5])

        shortest_path = list()

        for neighbor in [x for i, x in enumerate(boxes) if i != index]:

            neighbor_pos = (neighbor[4], neighbor[5])

            weighted_eucledian_distance = math.sqrt(
                pow((box_pos[0] - neighbor_pos[0])/2, 2) + pow((box_pos[1] - neighbor_pos[1]), 2))

            shortest_path.append(weighted_eucledian_distance)

            print(
                f'Index: {index}  Box: {box[-1]} {box_pos}  Neighbor: {neighbor[-1]} {neighbor_pos}  Distance: {weighted_eucledian_distance}')

        shortest_path.sort()
        shortest_path = shortest_path[:1]

        print(shortest_path)


def fuzzy_compare(blank_words: list, recognized_words: list):
    pass


def post_process(boxes: list):

    print('___ POST-PROCESS ___')

    group_fields(boxes)
