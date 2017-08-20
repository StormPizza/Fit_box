


# TkInter is a Python interface for Tk
from tkinter import *
from tkinter import ttk
import time
import random
start_time = time.time()

import math
import copy

def E1_part1_get_grad_type(dx, dy):
    # This considers it uninverted though
    # OUTPUT: "Q1", "Q2","Q4", "Q3", or "HORIZONTAL"
    types = [["Q1", "Q2"],["Q4", "Q3"]]
    # Q1 and Q2 with dy > 0
    # Q3 and Q4 with dy < 0
    # Q2 and Q3 with dx < 0
    # Q1 and Q4 with dx > 0
    type_index1 = 0  # [dx = -1, dy = 1]
    type_index2 = 0  # [dx = -1, dy = 1]
    if dx == 0:
        if dy > 0:
            return "Q12"
        else:  # dy < 0
            return "Q34"
    elif dx < 0:
        type_index2 = 1

    if dy == 0:
        if dx > 0:
            return "Q41"
        else:  # dx < 0
            return "Q23"
    elif dy < 0:
        type_index1 = 1
    return types[type_index1][type_index2]

#   PART 3     //////////////////
def E1_get_line_seg_grad(coord_1, coord_2, old_line_seg, y_axis_orient):
    # INPUT: new points and line segment data from old
    # OUTPUT: new line segment data

    # Part 1 - get the gradient     # coord_1 = [0, 0],   coord_2 = [1, 1]
    dy = (coord_2[1] - coord_1[1])
    dx = (coord_2[0] - coord_1[0])
    if dx == 0:
        new_gradient = "INFINITE"
    else:
        new_gradient = dy / dx
    # print(new_gradient)

    # Part 2 - get the gradient type / Quadrant (Q1, Q2, Q3, Q4, Horizontal)
    new_grad_type = E1_part1_get_grad_type(dx, dy)

    # Part 3 - get the new edge side
    ccw_side = {"Q1": ["up", "left"], "Q12": [None, "left"],
                "Q2": ["down", "left"], "Q23": ["down", None],
                "Q3": ["down", "right"], "Q34": [None, "right"],
                "Q4": ["up", "right"], "Q41": ["up", None]}

    # edge_side refers to the direction to go outside of polygon
    # priority goes to saying "left, right" instead of "up, down"
    if ccw_side[new_grad_type][1] is not None:
        new_edge_side = ccw_side[new_grad_type][1]
    else:
        new_edge_side = ccw_side[new_grad_type][0]

    # Part 4 - adjust for inverted y-axis
    up_down = ["up", "down"]
    # with an inverted y-axis, all up is down, and all down is up
    if y_axis_orient == "INVERTED" and new_edge_side in up_down:
        new_edge_side = up_down[up_down.index(new_edge_side)-1]

    new_line_seg = [coord_1, coord_2, new_gradient, new_grad_type, new_edge_side]
    return new_line_seg

# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////

def E2_part1_get_nearest_whole(upper_lower, edge_side):  # 1.6
    # print([ round(i) for i in upper_lower])
    rounded_num = int( sum(upper_lower)/len(upper_lower) )
    # print(upper_lower,rounded_num, "OLD ROUNDED NUM")
    # WHEN USING UPPER LOWER LIMIT, which has 2 values
    thick = 0.5  # dist from pixel center to pixel edge
    margin = 0.1  # extra gap surrounding shape               <---  MARGIN HERE
    # margin is fraction of whole pixel - pixel is 1x1
    if edge_side in ["left", "up"]:  # favors -1
        # if any part of the pixel edge is not outside of polygon, bump it
        # this first cond below never happens, so we adjust (+1)
        rounded_num += 1
        if True in [rounded_num - thick > i - margin for i in upper_lower]:
            rounded_num -= 1
        # if all of the pixel is out of the polygon, there is wastage, pull it
        elif False not in [rounded_num + thick < i for i in upper_lower]:
            rounded_num += 1
    elif edge_side in ["right", "down"]:  # favors +1
        # if any part of the pixel edge is not outside of polygon, bump it
        if True in [rounded_num + thick < i + margin for i in upper_lower]:
            rounded_num += 1
        # if all of the pixel is out of the polygon, there is wastage, pull it
        elif False not in [rounded_num - thick > i for i in upper_lower]:
            rounded_num -= 1
    # print( rounded_num, "NEW ROUNDED NUM")
    return rounded_num

def E2_part2_go_thru_y(line_seg, edge_points):
    # This takes a line segment and gives all the points along the line segment
    # on the OUTSIDE of the polygon
    x1, y1 = line_seg[0][0], line_seg[0][1]
    x2, y2 = line_seg[1][0], line_seg[1][1]
    dydx = line_seg[2]
    if y2 < y1:  # starting y should be lower than ending y
        y_range = reversed(range(int(y2), int(y1 + 1)))
    else:
        y_range = range(int(y1), int(y2 + 1))

    if line_seg[2] == "INFINITE":
        new_x = line_seg[0][0]
        new_x_2 = E2_part1_get_nearest_whole([new_x], line_seg[4])
        for i in y_range:
            new_y = i
            edge_points.append([new_x_2, new_y])
    else:
        for i in y_range:
            new_y = i
            new_x_r1 = ((new_y - y1 - 0.5) / dydx) + x1
            new_x_r2 = ((new_y - y1 + 0.5) / dydx) + x1
            new_x_2 = E2_part1_get_nearest_whole([new_x_r1, new_x_r2], line_seg[4])
            edge_points.append([new_x_2, new_y])

    # print(new_y, new_x, new_x_2)
    return edge_points


def E2_part3_go_thru_x(line_seg, edge_points):
    x1, y1 = line_seg[0][0], line_seg[0][1]
    x2, y2 = line_seg[1][0], line_seg[1][1]
    dydx = line_seg[2]
    if x2 < x1:
        x_range = reversed(range(int(x2), int(x1 + 1)))
    else:
        x_range = range(int(x1), int(x2 + 1))

    if line_seg[2] == 0:
        only_y = line_seg[0][1]
        new_y_2 = E2_part1_get_nearest_whole([only_y], line_seg[4])
        # print(line_seg, x_range, "LOOK ")
        for i in x_range:
            new_x = i
            edge_points.append([new_x, new_y_2])
    else:
        # print(line_seg, x_range, "LOOK 2")
        # print(int(x2), int(x1), "HERE")
        for i in x_range:
            # print(i, "E2_part3_go_thru_x")
            # print(line_seg, "E2_part3_go_thru_x")
            new_x = i
            new_y_r1 = ((new_x - x1 - 0.5) * dydx) + y1
            new_y_r2 = ((new_x - x1 + 0.5) * dydx) + y1
            new_y_2 = E2_part1_get_nearest_whole([new_y_r1, new_y_r2], line_seg[4])
            edge_points.append([new_x, new_y_2])
            # print(new_y_r1,new_y_r2,"E2_part3_go_thru_x")
            # print(edge_points, "new_y_r1")

        # print(new_y, new_x, new_x_2)
    return edge_points

def E2_part4_add_to_edge_dict(line_seg, edge_list, edge_outside, edge_dict):
    # This gets the list of points for this specific edge, and adds it to
    # edge dict
    # tried as much as possible to make only 1 of each y-position per edge
    # create a dict with { [y1]: [x1,x6]}
    # where we will fill from starting pt (x1,y1) to ending pt (x6,y1)
    # print(edge_dict, edge_list, "EDGE CIDT AND LIST")
    # IF HORIZONTAL
    if line_seg[2] == 0:  # gradient
        x_list = []
        y_value = edge_list[0][1]  # all y-values will be the same
        # we want to only get the x value, since the y-values will not change
        x_list = [i for [i, j] in edge_list]
        if y_value not in edge_dict:
            # edge_dict[y_value] = [min(x_list)]
            edge_dict[y_value] = [[min(x_list)], [edge_outside[0]]]
        else:
            # if y_value == 29:
            #     print("HERE", edge_dict)
            if min(x_list) not in edge_dict[y_value]:
                edge_dict[y_value].append(min(x_list))
            # edge_dict.setdefault(y_value, min(x_list))
            if max(x_list) not in edge_dict[y_value]:
                edge_dict[y_value].append(max(x_list))
            # edge_dict.setdefault(y_value, max(x_list))
    # IF ANY OTHER DIAGONAL LINE
    else:   # if this is the first of this "y", add the x as starting point
        for i in range(len(edge_list)):   # print(edge_list, edge_dict)
            new_y = edge_list[i][1]
            new_x = edge_list[i][0]
            # print(edge_dict, new_y)
            # print(edge_list)
            # if new_y == 29 and new_y not in edge_dict:
            #     print("HERE2", edge_dict)
            if new_y not in edge_dict:
                edge_dict[new_y] = [[new_x], [edge_outside[i]]]
            # if that exact point is already in the dict
            elif new_x in edge_dict[new_y][0]:
                index1 = edge_dict[new_y][0].index(new_x)
                if edge_dict[new_y][1][index1] != edge_outside[i]:
                    edge_dict[new_y][1][index1] = "both"
            else:  # len(edge_dict[edge_list[i+1]]) == 2:
                edge_dict[new_y][0].append(new_x)
                edge_dict[new_y][1].append(edge_outside[0])
    return edge_dict

#   PART 2     //////////////////
def E2_get_edge_pts(line_seg, edge_dict):  # modify to include the points themselves
    edge_points = []
    # ADD STARTING POINT
    start_x = E2_part1_get_nearest_whole( [line_seg[0][0]], line_seg[4] )
    start_y = E2_part1_get_nearest_whole( [line_seg[0][1]], line_seg[4] )
    edge_points.append([start_x, start_y])

    # this is preserve the order of number in the direction pt 1 to pt 2
    if line_seg[2] == "INFINITE":   # TBD
        E2_part2_go_thru_y(line_seg, edge_points)
    elif line_seg[2] == 0:
        # print(line_seg, "this went through zero")
        edge_points = E2_part3_go_thru_x(line_seg, edge_points)
    else:   # line_seg[3] in ["Q1", "Q2","Q4", "Q3"]:
        if abs(line_seg[2]) > 1:
            edge_points = E2_part2_go_thru_y(line_seg, edge_points)
        else:  # if the gradient is the opposite of steep
            line_seg_temp = copy.deepcopy(line_seg)
            if line_seg_temp[2] > 0:
                if line_seg_temp[4] == "right":
                    line_seg_temp[4] = "up"
                else:  # line_seg_temp[4] == "left":
                    line_seg_temp[4] = "down"
            else:  # if line_seg_temp[2] > 0:
                if line_seg_temp[4] == "right":
                    line_seg_temp[4] = "down"
                else:  # line_seg_temp[4] == "left":
                    line_seg_temp[4] = "up"
            edge_points = E2_part3_go_thru_x(line_seg_temp, edge_points)

    # ADD ENDING POINT
    end_x = E2_part1_get_nearest_whole( [line_seg[1][0]], line_seg[4] )
    end_y = E2_part1_get_nearest_whole( [line_seg[1][1]], line_seg[4] )
    edge_points.append([end_x, end_y])

    edge_outside = [line_seg[4] for i in edge_points]
    edge_dict = E2_part4_add_to_edge_dict(line_seg, edge_points, edge_outside, edge_dict)
    # print(line_seg)
    # print(edge_points)
    # print(edge_outside)
    # print(edge_dict)
    return edge_dict


# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////

# def E2_part4_add_to_edge_dict(edge_dict_temp, edge_dict):
#     for key, value in edge_dict_temp.items():
#         if key not in edge_dict:
#             edge_dict[key] = value
#         else:
#             edge_dict[key].extend(value)
#     return edge_dict

def E3_part1_add_to_approx_list(t_x, t_y, approx_points):
    for i_temp in range(int(len(approx_points)/2)):
        i = i_temp*2
        have_read = [approx_points[i], approx_points[i+1]]
        look_for = [t_x, t_y]
        if have_read == look_for:
            return approx_points
    approx_points.append(t_x)
    approx_points.append(t_y)

    return approx_points

#   PART 3     //////////////////
def E3_convert_dict_to_points(edge_dict):
    approx_points = []

    for i in range(max(edge_dict)+1):  # for each value of y
        if i not in edge_dict:  # in case the first point isnt zero
            continue
        t_y = i

        # sorting from lowest to highest y-position starting from 0
        t_x_list = edge_dict[i][0]
        t_x_side_list = edge_dict[i][1]
        x_zip = list(zip(t_x_list, t_x_side_list))[:]
        x_zip.sort()
        t_x_list2 = [x for (x,y) in x_zip]
        t_x_side_list2 = [y for (x,y) in x_zip]

        # If there are duplicates, left goes before right
        x_hold = None
        for j in range(len(t_x_list)):
            if t_x_list2[j] == x_hold:
                if [t_x_side_list2[j-1], t_x_side_list2[j]] == ['right', 'left']:
                    [t_x_side_list2[j-1], t_x_side_list2[j]] == ['left', 'right']
            x_hold = t_x_list2[j]

        # now going through the list and adding to approx_points
        left_value = ""
        for k in range(len(t_x_list2)):
            approx_points = E3_part1_add_to_approx_list(t_x_list2[k], t_y, approx_points)
            if t_x_side_list2[k] == "left":
                left_value = t_x_list2[k]
            elif t_x_side_list2[k] == "right":
                right_value = t_x_list2[k]
                if left_value != "":
                    for t_x in range(left_value, right_value):
                        approx_points = E3_part1_add_to_approx_list(t_x, t_y, approx_points)
                    left_value = t_x

    return approx_points


def E_final_generate_approx(orig_points):

    line_seg = [None, None, None, "Q3", "left"]

    edge_dict = {}  # Edge dict is the main output here
    # print(orig_points)
    for iii in range(int(len(orig_points)/2)-1):  # for every adjacent pair of coords
        i = 2*iii
        coord_1 = [orig_points[i], orig_points[i+1]]
        coord_2 = [orig_points[i+2], orig_points[i+3]]
        line_seg = E1_get_line_seg_grad(coord_1, coord_2, line_seg, "INVERTED")
        edge_dict = E2_get_edge_pts(line_seg, edge_dict)
    approx_points = E3_convert_dict_to_points(edge_dict)
    return approx_points
