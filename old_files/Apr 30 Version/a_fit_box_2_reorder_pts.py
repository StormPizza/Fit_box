


# TkInter is a Python interface for Tk
from tkinter import *
from tkinter import ttk
import time
import random
start_time = time.time()

import math
import copy


# /////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////
#    PART   A   ///////////////////////////////////////////////////////////////

def C1_make_points_counter_clockwise(points_list, y_axis_orient = "INVERTED"):
    # print(points_list)
    # INPUT: list of points, and whether or not we have inverted axis or not
    #        the inverted y-axis is typical in html, and svg and in tkinter
    # OUTPUT: the list of points but in the Counter Clockwise order, same start pt
    cc_check = 0
    for j in range(int(len(points_list)/2)-1):
        # print(cc_check, j)
        i = 2*j
        factor1 = points_list[i+2] - points_list[i]
        factor2 = points_list[i+3] + points_list[i+1]
        cc_check += (factor1 * factor2)
    factor1 = points_list[0] - points_list[-2]
    factor2 = points_list[1] - points_list[-1]
    cc_check += (factor1 * factor2)
    # for regular y-axis, negative cc_check means counterclockwise
    if y_axis_orient == "INVERTED":
        cc_check *= -1

    if cc_check > 0:
        # print(cc_check, "CC_CHECK")
        # points_list.reverse()
        # points_list.insert(0, points_list.pop(-1))
        new_points_list = []
        for j2 in reversed(range(int(len(points_list)/2))):
            new_points_list.append(points_list[j2*2])
            new_points_list.append(points_list[(j2*2)+1])
            # print(new_points_list, "THIS POINT LIST")
        points_list = new_points_list
    # print(cc_check)
    # print(points_list, "COUNTER CLOCK")
    return points_list

def C2_choose_left_up_point(points_list, y_axis_orient = "INVERTED"):
    # INPUT: list of points, and whether or not we have inverted axis or not
    #        the inverted y-axis is typical in html, and svg and in tkinter
    # OUTPUT: the list of points starting with leftmost-up-most point
    # This is used later so that we know for certain that outside of
    # of polygon is on the left - for the benefit of E1_get_line_segment()
    min_x = points_list[0]
    min_x_index_list = []
    for j in range(int(len(points_list)/2)):    # print(cc_check, j)
        if points_list[2*j] <= min_x:
            min_x = points_list[2*j]
    for j2 in range(int(len(points_list)/2)):    # print(cc_check, j)
        if points_list[2*j2] <= min_x:
            # print(min_x, points_list[i], "second is less")
            min_x_index_list.append(2*j2)

    # print(min_x_index_list, "min_x_index_list")
    if y_axis_orient == "INVERTED":  # look for minimum x
        # print("1")
        min_y = points_list[min_x_index_list[0]+1]
        min_x_index = 0
        # min_x_index_list_2 = []
        for k in range(len(min_x_index_list)):
            # item_list = min_x_index_list[k]
            if points_list[min_x_index_list[k]+1] <= min_y:
                min_y = points_list[min_x_index_list[k]+1]
                min_x_index = min_x_index_list[k]
                new_index = min_x_index
            # print(min_y, "MIN Y", new_index, "new_index")
    else:
        # print("2")
        max_y = points_list[min_x_index_list[0]+1]
        max_x_index = 0
        # max_x_index_list_2 = []
        for k in range(len(min_x_index_list)):
            # item_list = max_x_index_list[k]
            if points_list[min_x_index_list[k]+1] >= max_y:
                max_y = points_list[min_x_index_list[k]+1]
                max_x_index = min_x_index_list[k]
                new_index = max_x_index
    # Fix points by making that index go first
    points_list = points_list[new_index:] + points_list[:new_index]
    # print(points_list, "END OF CC CONVERT ")
    return points_list

def C3_remove_duplicates(points_list):
    # this removes duplicates WHEN THEY COME ONE AFTER THE OTHER
    for i_temp in reversed(range(int(len(points_list)/2)-1)):
        i = i_temp*2
        check1 = [points_list[i], points_list[i+1]]
        check2 = [points_list[i+2], points_list[i+3]]
        if check1 == check2:
            points_list.pop(i)
            points_list.pop(i)
    return points_list

def C4_close_loop(points_list1):
    # this makes the first coordinates and last coordinates be the same
    points_list1.extend(points_list1[:2])
    return points_list1

# /////////////////////////////////////////////////////////////////////////////
def C_final_rearrange_points(orig_points):
    # y_axis_orient = "INVERTED"
    orig_points = C1_make_points_counter_clockwise(orig_points)
    orig_points = C2_choose_left_up_point(orig_points)
    orig_points = C3_remove_duplicates(orig_points)
    orig_points = C4_close_loop(orig_points)
    return orig_points
