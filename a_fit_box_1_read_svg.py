


# TkInter is a Python interface for Tk
from tkinter import *
from tkinter import ttk
import time
import random
start_time = time.time()

import math
import copy
import re

# AB_OR_REL = "ABSOLUTE"  # Absolute or Relative (for process1)
mark_list = []  # (for process1)
new_list_marker = []  # (for process1)

# gg = lambda x: print(x)  # to test if lambda can be called from import
#      PART A - X    ///////////////////////////////////////
def is_number(letter):
    '''By putting this initial sentence in triple quotes, you can
    access it by calling myFunc.__doc___'''
    return isinstance(letter, int)
    # try:
    #     int(letter)
    #     return "NUMBER"
    # except:
    #     return "LETTER"
#      PART B - X   ///////////////////////////////////////
# some functions I copied, and barely know how works
# INPUT: list with 3 or 4 tuples
def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            # print(xys)
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n):    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:     # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result

# ////////////////////////////////////////////////////////////////////////
#                  P0                   /////////////////////////////////
#      PART A    ///////////////////////////////////////
# modify this to allow "path" to be divided to many lines
def read_the_svg_file(filename):
    #read_the_svg_file(String):
    # INPUT - svg filename (shield.svg)
    # OUTPUT - String[][] list with entries where "<path" or "<rect" was found
    print("TAKING FROM ", filename)
    target = open(filename, "r")
    path_list = []  # list of polygons(paths)
    is_in_comment = 0  # the number shows is within how many commented loops
    IN_PATH = False
    for next_line in target:
        next_line = next_line.strip(" ").strip("\n").strip("\r")

        # CHECK FOR COMMENT <!-- -->
        if "-->" in next_line and is_in_comment > 0:
            next_line = next_line[next_line.index("-->")+2:]
            is_in_comment -= 1
        if "<!--" in next_line:
            is_in_comment += 1
            if "-->" in next_line and next_line.index("<!--") < next_line.index("-->"):
                next_line_end = next_line[next_line.index("-->")+2:]
                next_line_start = next_line[:next_line.index("<!--")]
                next_line = next_line_start + next_line_end
                is_in_comment -= 1
                continue
        if is_in_comment > 0:
            continue

        # START THE COPY
        if "<path" in next_line:
            IN_PATH = True
            path_list.append(next_line)
            if "/>" in next_line and next_line.index("<path") < next_line.index("/>"):
                IN_PATH = False
            continue
        if IN_PATH is True:
            path_list[-1] += " " + next_line
            if "/>" in next_line:
                IN_PATH = False
    return path_list
# ////////////////////////////////////////////////////////////////////////
#                  P1                   /////////////////////////////////
# used in P1_turn_str_to_list
def add_items(temp_num, marker, c_list, mark_list):
# def add_items(String, String, int[], String[]):
    if not temp_num:
        return [c_list, mark_list]
    c_list.append(float(temp_num))
    mark_list.append(marker)
    #      [ int[], String[] ]
    return [c_list, mark_list]

def P1_turn_str_to_list(raw_string):
    # INPUT: string, one of the list items in new_list
    #       a very long string that begins with "<path" from svg file
    #       from there the coord numbers are picked off and added to c_list
    #       some are marked as "C" to be converted into curves later
    #       INPUT EXAMPLE : raw_string = "<path style=.....d="m 71,56 19,21 45,11....."
    # OUTPUT: list, list of points in the string, also letters (c) marklist
    # OUTPUT: int[]    c_list = [69, 912, 249, 950, 443, 841]
    # OUTPUT: String[] m_list = ['M', 'M', 'M', 'M', 'L', 'L']
    [c_list, temp_num] = [[], ""]
    # c_list is the list of numerical coordinates
    # [69, 912, 249, 950, 443, 841] has 2 coordinate pairs
    #  "temp_num" goes in c_list
    [m_list, marker] = [[], ""]
    # m_list is the list of markers in the form of letters - see letters
    # ['M', 'M', 'M', 'M', 'L', 'L']
    #  "marker" goes in c_list
    print("P1" + raw_string)
    TYPES_OF_START = ["path", "circ", "rect"]  # might be outside of method
    letters = ["M", "L", "H", "V", "C", "S", "Q", "T"]
    # M(start),, L(line), H(horiz), V(vert),
    # C(curve 3pts), S(curve-1pt, follow C), Q(curve 2pts), T(curve-1pt, follow Q)
    if raw_string[:5] == "<path":
        # \w+ picks out "style", [=] picks out =
        # [^"]+ picks out non-quotation marks, and more than 1
        # raw_list = ['style="tgdfg" ', 'd="m0 0 1 1" ', '']
        raw_list = re.split('(\w+[=]["][^"]+["][ ])', raw_string)
        # String[] raw_list
        long_string = [i[3:-2]for i in raw_list if i[:2] == "d="][0]
        # look for the first string that starts with "d=", and take that
        # String long_string = 'm0,0 1,1 '
        long_string = long_string.replace(",", " ")    # print(raw_string)
        # String long_string = 'm0 0 1 1 '
        for digit in long_string:
            # print("CURRENT LTTER IS", long_string[i])
            if digit == "-":
                temp_num = digit + temp_num
            elif digit == " ":  # all the commas have been replaced
                if temp_num == "-":
                    continue
                [c_list, m_list] = add_items(temp_num, marker, c_list, m_list)
                temp_num = ""
            elif digit.upper() in letters:
                [c_list, m_list] = add_items(temp_num, marker, c_list, m_list)
                marker = digit  # this before marker
                temp_num = ""
            elif digit.upper() in ["Z", '"']:
                [c_list, m_list] = add_items(temp_num, marker, c_list, m_list)
                marker = digit
                temp_num = ""
                return [c_list, m_list]
            else:  # the remaining is single digit
                temp_num += digit
                # print("temp_word2", temp_word, i, long_string[i])
    # c_list = [round(i) for i in c_list]
    return [c_list, m_list]  # we actually use return at "elif z"

# "M 45.7,95.2 42.8,460 c 0,0 277.1,85 239.9,-91 C 245,192 45.7,95.2 45.7,95.2 h -95.7 v
# 0 0,-45.2 z"
def P1_b_turn_relative_to_absolute(c_list_item, mark_list_item):
    #  def P1_b_turn_relative_to_absolute(c_list_item, mark_list_item):
    # sometimes coord are represented in relative terms, we convert to abs
    # print(c_list_item, "IN P1_b")
    # print(mark_list_item, "IN P1_b")
    C_ORIG_COUNT = 6
    c_count = C_ORIG_COUNT  # 6 5,  4 3,  2 1
    S_ORIG_COUNT = 4
    s_count = S_ORIG_COUNT  # 6 5,  4 3,  2 1
    base_coord = [c_list_item[0], c_list_item[1]]  # will update
    tic_toc = [1, 0]  # this works in conjunction with base_count
    base_count = 0
    # base_y = c_list_item[1]
    for i in range(2, len(c_list_item)):  # we dont convert the first pair
        # print(c_list_item, "IN P1_b")
        # print(mark_list_item, "IN P1_b")
        if mark_list_item[i].islower():
            if mark_list_item[i].upper() == "C":
                if c_count <= 0:
                    c_count = C_ORIG_COUNT
                new_coord = c_list_item[i] + base_coord[base_count]
                c_list_item[i] = new_coord
                if c_count <= 2:  # last two coords are final point
                    base_coord[base_count] = new_coord
                c_count -= 1
                base_count = tic_toc[base_count]  # toggles between 0 and 1
            # elif mark_list_item[i].upper() == "S" or mark_list_item[i].upper() == "Q":
            elif mark_list_item[i].upper() in ["S", "Q"]:
                if s_count <= 0:
                    s_count = S_ORIG_COUNT
                new_coord = c_list_item[i] + base_coord[base_count]
                c_list_item[i] = new_coord
                if s_count <= 2:  # last two coords are final point
                    base_coord[base_count] = new_coord
                s_count -= 1
                base_count = tic_toc[base_count]  # toggles between 0 and 1
            elif mark_list_item[i].upper() == "H":
                c_list_item[i] += base_coord[0]
                base_coord[0] = c_list_item[i]
                base_count = 0  # Reset counter
            elif mark_list_item[i].upper() == "V":
                c_list_item[i] += base_coord[1]
                base_coord[1] = c_list_item[i]
                base_count = 0  # Reset counter
                # print(base_count, base_coord, "THISS P1b")
            else:  # "m", "L", "z", "t"
                # print(base_count, base_coord, "P1b")
                c_list_item[i] += base_coord[base_count]
                base_coord[base_count] = c_list_item[i]
                base_count = tic_toc[base_count]  # toggles between 0 and 1
            mark_list_item[i] = mark_list_item[i].upper()
        else:  # if we find uppercase instead
            if mark_list_item[i].upper() == "H":
                base_coord[0] = c_list_item[i]
                base_count = 0  # Reset counter
            elif mark_list_item[i].upper() == "V":
                base_coord[1] = c_list_item[i]
                base_count = 0  # Reset counter
            else:
                base_coord[base_count] = c_list_item[i]
                base_count = tic_toc[base_count]  # toggles between 0 and 1

    return [c_list_item]

def P2b_convert_S_to_C(path_list_item, mark_list_item):
    S_count = 0  # when this hits 3, stuff happens
    # print (path_list_item, mark_list_item, "HERE P2b")
    for j in reversed(range(len(mark_list_item))):
        if mark_list_item[j].upper() == "S":
            S_count += 1
            if S_count >= 4:
                # PATH LIST - CONVERT
                ctrl_curve_x = path_list_item[j-4]
                ctrl_curve_y = path_list_item[j-3]
                end_x = path_list_item[j-2]
                end_y = path_list_item[j-1]
                new_ctrl_pt_x = (2 * end_x) - ctrl_curve_x
                new_ctrl_pt_y = (2 * end_y) - ctrl_curve_y
                path_list_item.insert(j, new_ctrl_pt_y)
                path_list_item.insert(j, new_ctrl_pt_x)
                # MARK LIST - CONVERT
                mark_list_item[j:j+3] = ["C" for i in range(6)]
                S_count = 0
    # print (path_list_item, mark_list_item, "HERE P2b")
    return [path_list_item, mark_list_item]

def P2c_convert_T_to_Q(path_list_item, mark_list_item):
    T_count = 0  # when this hits 3, stuff happens
    # print (path_list_item, mark_list_item, "HERE P2c")
    for j in reversed(range(len(mark_list_item))):
        if mark_list_item[j].upper() == "T":
            T_count += 1
            if T_count >= 2:
                # PATH LIST - CONVERT
                ctrl_curve_x = path_list_item[j-4]
                ctrl_curve_y = path_list_item[j-3]
                end_x = path_list_item[j-2]
                end_y = path_list_item[j-1]
                new_ctrl_pt_x = (2 * end_x) - ctrl_curve_x
                new_ctrl_pt_y = (2 * end_y) - ctrl_curve_y
                path_list_item.insert(j, new_ctrl_pt_y)
                path_list_item.insert(j, new_ctrl_pt_x)
                # MARK LIST - CONVERT
                mark_list_item[j:j+1] = ["Q" for i in range(4)]
                T_count = 0
    # print (path_list_item, mark_list_item, "HERE P2c")
    return [path_list_item, mark_list_item]

def P2e_convert_C_Q_to_L(path_list_item, mark_list_item):
    # print(path_list_item, "IN P2e")
    # print(mark_list_item, "IN P2e")

    RESOLUTION = 8
    ts = [t/RESOLUTION for t in range(RESOLUTION+1)]
    # print(ts, "TS")
    # CURVE_COPY_C = False
    # CURVE_COPY_Q = False
    index_of_last_C = -1
    index_of_last_Q = -1
    # this goes through the mark_list complete and looks for "c"
    # for i in range(len(path_list)):
    # print(mark_list_item, "FOR THIS MARK LIST ITEM P2e")
    curve_list = []  # this will contain lists of pairs, rewritable
    # sample curve_list = [[2, 9]], "c" from index 2 to index 9 of list
    # Curve_start = 9999
    for j in range(len(mark_list_item)):
        # C is for curve, CURVE_COPY = False means C only found now
        # ['M', 'M', 'C', 'C', 'C', 'C', 'C', 'C',
        # if "C" is found, add index -2 to curvelist, and inc_listdex -2 + 7
        # then mark CURVE_COPY = True to ignore the next 5
        # if mark_list_item[j].upper() == "C" and CURVE_COPY_C == False:
        if mark_list_item[j].upper() == "C" and j > index_of_last_C:
            curve_list.append([j - 2, j - 2 + 7])
            index_of_last_C = j + 5
        # if mark_list_item[j].upper() == "Q" and CURVE_COPY_Q == False:
        if mark_list_item[j].upper() == "Q" and j > index_of_last_Q:
            curve_list.append([j-2, j-2+5])
            # curve_list[-1].append(j-2)  # start [0, X]
            # Curve_start = j
            index_of_last_Q = j + 3
            # curve_list[-1].append(j-2+5)  # end[X , 7]
            # minus 2 because x1y1 c x1y1 x2y2 x2y2
            # starting point is before "c"
            # CURVE_COPY_Q = True
        # this confirms there are 8x "c" in a row, and resets count

    # The curve_list is used to remove the "shortcut code" instances in the
    # path list, and replace it with its uncompressed formula
    # working from the end of the list makes it so that the change in index
    # will not affect the next "shortcut codes", because they rely on index
    for k in reversed(range(len(curve_list))):
        # print(path_list_item[4:10], "THIS PATH LIST")
        path_copy_for_bez = []  # make bez input
        # print(k, curve_list)
        for i4 in range(curve_list[k][0],curve_list[k][1]+1)[::2]:  # remove +1
        # for i4 in range(curve_list[k][0],curve_list[k][1]+1):  # remove +1
            # if i4 % 2 == 0:  # only even numbers
                # print(path_list_item[i4])
            entry1 = path_list_item[i4]
            entry2 = path_list_item[i4 + 1]
            path_copy_for_bez.append((entry1, entry2))
        bezier_temp = make_bezier(path_copy_for_bez)  # this is bez fn maker
        new_points2 = bezier_temp(ts)  # this is the bez fn... in d wrld
        # new_points2 = round_bez_output(new_points2)
        # print(len(new_points2))
        # print(path_copy_for_bez, "BEZ INPUT",k,"\n")
        # print([ path_list_item[i] for i in range(curve_list[0][0],curve_list[0][1])], "CURVE LIST 2")
        # print(new_points2, "BEZ OUTPUT",k,"\n")
        # print(" /////////////////////////////////////////////")
        for i2 in reversed(range(curve_list[k][0],curve_list[k][1]+1)):
            path_list_item.pop(i2)
            mark_list_item.pop(i2)
        # print(path_list_item, "AFTER POP","SEE INDEX",curve_list[k],"\n")
        for i3 in reversed(range(len(new_points2))):
            # print(path_list)
            path_list_item.insert(curve_list[k][0], new_points2[i3][1])
            path_list_item.insert(curve_list[k][0], new_points2[i3][0])
            # path_list_item.insert(curve_list[k][0], round(new_points2[i3][1],2))
            # path_list_item.insert(curve_list[k][0], round(new_points2[i3][0],2))
            # print(mark_list_item,new_points2,  "MARK")
            mark_list_item.insert(curve_list[k][0], "L")
            mark_list_item.insert(curve_list[k][0], "L")  # erases M

    # path_list_item = [round(i) for i in path_list_item]
    return [path_list_item, mark_list_item]

def P3_convert_V_H_to_L(path_list_item, mark_list_item):
    # print(path_list_item, "IN P3")
    # print(mark_list_item, "IN P3")
    # Converts vertical and horizontal - all "H" "V" will changes to "L"
    # hor_list = []  # list of indexes of horizontal
    # vert_list = []
    bump = 1
    # bad_list = ["V", "H"]  # this list used when "V" and "H" are referenced
    # ['M', 'M', *1'M', *2'M', 'V', 'H', 'V', 'H', 'V', 'L', 'L']  see *
    for j in reversed(range(len(mark_list_item))):
        if mark_list_item[j].upper() == "H":  # there is x, must add y
            while mark_list_item[j - bump].upper() == "H":
                bump += 1
            if mark_list_item[j - bump] == "V":  # "V is good to copy"
                path_list_item.insert(j+1, path_list_item[j-bump])
            else:
                path_list_item.insert(j+1, path_list_item[j-0-bump])  # *2'M'
            mark_list_item[j] = "L"
            mark_list_item.insert(j, "L")
        elif mark_list_item[j].upper() == "V":  # there is x, must add y
            while mark_list_item[j - bump].upper() == "V":
                bump += 1
            # print(bump, j, mark_list_item[j], path_list_item[j])
            if mark_list_item[j - bump] == "H":  # "H is good to copy"
                path_list_item.insert(j, path_list_item[j-bump])
            else:
                path_list_item.insert(j, path_list_item[j-1-bump])  # *1'M'
            mark_list_item[j] = "L"
            mark_list_item.insert(j, "L")
        bump = 1
    return [path_list_item, mark_list_item]

def P5_translate_some(path_list_item):
    # KEEPS THE IMAGE FROM APPEARING OFF SCREEN
    MARGIN = 50  # PIXEL SIZE
    # MIN_X = min([i for i in path_list_item if path_list_item.index(i)%2 == 0])
    # MIN_Y = min([i for i in path_list_item if path_list_item.index(i)%2 == 1])
    MIN_X = min(path_list_item[::2])
    MIN_Y = min(path_list_item[1::2])

    for k3 in range(int(len(path_list_item)/2)):
         path_list_item[2*k3] -= MIN_X - MARGIN
         path_list_item[(2*k3) + 1] -= MIN_Y - MARGIN
    return path_list_item

#/////////////////////////////////////////////////////////////////

def P_final_all_convert_svg_to_list(target_file):
    # INPUT: String "drawingtest7"
    # OUTPUT:
    path_list = read_the_svg_file(target_file)
    # to test S "d="m 71,56 19,21 45,11"
    mark_list = [ [] for item in path_list ]

    for j in range(len(path_list)):  # only runs through once for now
        [path_list[j], mark_list[j]] = P1_turn_str_to_list(path_list[j])
        [path_list[j]] = P1_b_turn_relative_to_absolute(path_list[j], mark_list[j])
        # print(path_list[j], "OUTSIDE P1b make abso")
        # print(path_list, "PATH LIST after translating", len(path_list[0]))

        [path_list[j], mark_list[j]] = P2b_convert_S_to_C(path_list[j], mark_list[j])
        [path_list[j], mark_list[j]] = P2c_convert_T_to_Q(path_list[j], mark_list[j])
        # print(path_list[j], "OUTSIDE P2b", len(path_list[j]))
        # print(mark_list[j], "OUTSIDE P2b", len(mark_list[j]))

        [path_list[j], mark_list[j]] = P2e_convert_C_Q_to_L(path_list[j], mark_list[j])
        [path_list[j], mark_list[j]] = P3_convert_V_H_to_L(path_list[j], mark_list[j])
        # print(path_list[j], "OUTSIDE P3")
        # print(mark_list[j], "OUTSIDE P3")
        # print(path_list[j], "AFTER CURVE CONVERSION")
        path_list[j] = P5_translate_some(path_list[j])

    if max(path_list[0]) > 100:
        path_list = [[int(i) for i in path_list[0]]]
    # print(path_list, "PATH LIST after translating", len(path_list[0]))
    return path_list
