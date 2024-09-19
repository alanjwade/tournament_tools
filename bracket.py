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
 
    for match_pos in range(0, int(num_people_first_round/2)):
        (x0, y0) = startpoints[(starting_round, match_pos)][0]
        (x1, y1) = startpoints[(starting_round, match_pos)][1]
        c.drawString(x0, y0,   people[people_pos]['Student First Name']
                             + ' '
                             + people[people_pos]['Student Last Name'])
        people_pos = people_pos + 1
        c.drawString(x1, y1,   people[people_pos]['Student First Name']
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
    
        (x0, y0) = startpoints[(starting_round + 1, math.floor(participant_pos / 2 ))][0]
        (x1, y1) = startpoints[(starting_round + 1, math.floor(participant_pos / 2 ))][1]
        if participant_pos % 2 == 0: # even
            c.drawString(x0, y0,   people[people_pos]['Student First Name'] 
                                 + ' '
                                 + people[people_pos]['Student Last Name'] )
            people_pos = people_pos + 1
        else: # odd
            c.drawString(x1, y1,   people[people_pos]['Student First Name'] 
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
        for line in range(0, lines_in_this_round):
            x_left = int(x_global_offset + x_width_per_round * (round-1))
            x_right = int(x_left + x_width_per_round)


    for round in range(1, rounds + 1):
        if round > 0:
            matches_in_this_round = int(2**(4-round))
        elif round == 5:
            matches_in_this_round = 1
        else:
            matches_in_this_round = int(0)



        y_height = 1/(2**round) * inch
        x_width = 1.5 * inch
        x_offset_per_round = 1.5
        x_start_this_round = ((round-1)  * x_offset_per_round * inch) + (0.5 * inch)


        for match in range(0, matches_in_this_round):
            x_start_this_round = ((round-1) * x_offset_per_round * inch) + (0.5 * inch)
            x_mid_this_round = x_start_this_round + x_offset_per_round/2
            y_mid_this_match = (0.5 * inch) + ((match+1) * y_height * 2)
            match_startpoint = make_match(c, x_global_offset, y_global_offset, x_width_per_round, y_height_first_round, round, match)

            startpoints[(round, match)] = match_startpoint

    # add teams
    # pp(startpoints)
    place_people(c, startpoints, people)

def make_3rd_place_bracket(c):
    pass
