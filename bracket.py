from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import math
from pprint import pprint as pp

def place_people(c, startpoints, people):
    people_number = len(people)

    people_log2_ceil = (people_number-1).bit_length()
    people_log2_floor = people_number.bit_length() - 1

    # Figure out the starting round
    starting_round = 5 - people_log2_ceil

    num_people_second_round = 2**people_log2_ceil - people_number
    num_people_first_round = people_number - num_people_second_round

    people_pos = 0

    # pp(people[0]['Student First Name'])
 
    for match_pos in range(0, int(num_people_first_round)):
        (x0, y0) = startpoints[(starting_round, match_pos)]
        c.drawString(x0, y0,   people[people_pos]['Student First Name']
                             + ' '
                             + people[people_pos]['Student Last Name'])
        people_pos = people_pos + 1

    # There are only full matches in the first round, so an even number.
    # However, in the second round, there could be either an even or odd
    # number of participants to be placed first.
    matches_in_first_round = int(num_people_first_round/2)

    total_matches_in_second_round = 2**(3-starting_round)
    total_participant_slots_in_second_round = int(total_matches_in_second_round * 2)

    # matches are 1 based
    # 

    # 0 based
    starting_participant_pos_in_second_round = total_participant_slots_in_second_round - num_people_second_round

    for participant_pos in range(starting_participant_pos_in_second_round, \
                                 starting_participant_pos_in_second_round + num_people_second_round):
    
        (x0, y0) = startpoints[(starting_round + 1, math.floor(participant_pos))]

        c.drawString(x0, y0,   people[people_pos]['Student First Name'] 
                                + ' '
                                + people[people_pos]['Student Last Name'] )
        people_pos = people_pos + 1
        

    

def make_match(c, x_global_offset, y_global_offset, x_width_per_round, y_height_first_round, round, match):

    # Define the box
    x_left = int(x_global_offset + x_width_per_round * (round-1))
    x_right = int(x_left + x_width_per_round)

    #            floor of the bracket  + initial y offset  * start of this one
    y_bottom = int(y_global_offset + (2**(round - 1) * y_height_first_round/2) + ((match) * 2**round * y_height_first_round))
    y_top = int(y_bottom + (2**(round - 1) * y_height_first_round))

    if round == 5:
        c.line(x_left, y_bottom, x_right, y_bottom)

    else:
        c.line(x_left, y_bottom, x_right, y_bottom)
        c.line(x_right, y_bottom, x_right, y_top)
        c.line(x_left, y_top, x_right, y_top)

    # c.showPage()
    # c.save()
    # exit()
    return ((x_left, y_bottom), (x_left, y_top))

def make_bracket(c, people, virt_ring):
    '''Make one bracket, populated with a given list of teams (people).'''
    
    rounds = 5
    x_global_offset = 0.5 * inch
    y_global_offset = 0.5 * inch
    x_width_per_round = 1.5 * inch
    y_height_first_round = 0.6 * inch

    c.drawImage("watermark.png", 0, 0, mask="auto")

    startpoints = dict()

    for round in range(1, rounds + 1):

        # draw the right number of participants in this round
        lines_in_this_round = 2**(rounds-round)

        # This is the y distance between lines in the same round
        y_height = y_height_first_round * 2**(round-1)

        # This is the starting offset for this round
        y_offset_this_round = y_height_first_round/2 * 2**(round-1)

        x_offset_per_round = 1.5
        x_start_this_round = ((round-1)  * x_offset_per_round * inch) + (0.5 * inch)

        for linenum in range(0, lines_in_this_round):
            x_left = int(x_global_offset + x_width_per_round * (round-1))
            x_right = int(x_left + x_width_per_round)

            y = y_global_offset + y_offset_this_round+ (linenum * y_height) 

            c.line(x_left, y, x_right, y)

            if linenum %2 == 1:
                # The top one of a match
                c.line(x_right, y, x_right, y-y_height)

            startpoints[(round, linenum)] = (x_left, y)

 
    # add teams
    # pp(startpoints)
    place_people(c, startpoints, people)

def make_3rd_place_bracket(c):
    pass
