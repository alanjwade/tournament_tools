from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import math
from pprint import pprint as pp
import tt_global as tt
from collections import namedtuple

def place_people(c, startpoints, people, match_coord):
    people_number = len(people)

    people_log2_ceil = (people_number-1).bit_length()
    people_log2_floor = people_number.bit_length() - 1
    rounds = 5
    # Figure out the starting round
    starting_round = 5 - people_log2_ceil
    second_round = starting_round + 1

    num_people_second_round = 2**people_log2_ceil - people_number
    num_people_first_round = people_number - num_people_second_round

    people_pos = 0

    # pp(people[0]['Student First Name'])

    # The list of positions to put the 'match #' string
    match_str_arr = list()
 
    # There are only full matches in the first round, so an even number.
    # However, in the second round, there could be either an even or odd
    # number of participants to be placed first.
    matches_in_first_round = int(num_people_first_round/2)

    total_matches_in_second_round = 2**(3-starting_round)
    total_participant_slots_in_second_round = int(total_matches_in_second_round * 2)
 
    # matches and startpoints are numbered per round, from 0, from the bottom.
    # 

    # 0 based
    starting_participant_pos_in_second_round = total_participant_slots_in_second_round - num_people_second_round

    # Start with the participants in the second round, so the first person in
    # the people list is at the top.
    for match_pos in range(total_participant_slots_in_second_round - 1, \
                           total_participant_slots_in_second_round - 1 - num_people_second_round, \
                           -1):
    
        (x0, y0) = startpoints[(second_round, match_pos)]

        c.drawString(x0, y0,   people[people_pos]['Student First Name'] 
                                + ' '
                                + people[people_pos]['Student Last Name'] )
        people_pos = people_pos + 1
        
    # Then go back a round and add the rest.
    # Here we'll discover what the first match is.
    for match_pos in range(num_people_first_round -1, \
                           -1, -1):
        (x0, y0) = startpoints[(starting_round, match_pos)]
        c.drawString(x0, y0,   people[people_pos]['Student First Name']
                             + ' '
                             + people[people_pos]['Student Last Name'])
        people_pos = people_pos + 1

        # This is the first match
        

    match_num = 1

    # place the 'match #' text. The third place match goes before the first place match,
    # so special case that.
    for match_str_round in range(starting_round, rounds-1):
    
        if match_str_round == starting_round:
            starting_match_num = math.floor((num_people_first_round/2)) -1
        else:
            starting_match_num = 2**(rounds - match_str_round - 1) - 1

        for match_str_match in range(starting_match_num, -1, -1):
            match_coord[(match_str_round, match_str_match)]['match str'] = 'Match {}'.format(match_num)
            x = match_coord[(match_str_round, match_str_match)]['startx']
            y = match_coord[(match_str_round, match_str_match)]['midy']
            c.drawString(x, y, match_coord[(match_str_round, match_str_match)]['match str'])
            match_num += 1
    
    # Handle the third place match
    if len(people) > 2:
        match_coord[(rounds, 0)]['match str'] = 'Match {}'.format(match_num)
        x = match_coord[(rounds, 0)]['startx']    
        y = match_coord[(rounds, 0)]['midy']
        c.drawString(x, y, match_coord[(rounds, 0)]['match str'])
        match_num += 1

    # Handle the first place match
    match_coord[(rounds-1, 0)]['match str'] = 'Match {}'.format(match_num)
    x = match_coord[(rounds-1, 0)]['startx']    
    y = match_coord[(rounds-1, 0)]['midy']
    c.drawString(x, y, match_coord[(rounds-1, 0)]['match str'])
    match_num += 1



def make_bracket(c, people, virt_ring, phys_ring, level):
    '''Make one bracket, populated with a given list of teams (people).'''
    
    rounds = 5
    x_global_offset = int(0.5 * inch)
    y_global_offset = int(0.5 * inch)
    x_width_per_round = int(1.5 * inch)
    y_height_first_round = int(0.6 * inch)

    c.drawImage("watermark.png", .5*inch, 0, mask="auto")

    c.drawString(inch, 10*inch, virt_ring)


    fg, bg = tt.get_ring_colors(phys_ring)

    t = Table([[level + ' ' + tt.ring_name_expanded(phys_ring)]], 5*inch, .7*inch)
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (0,0), bg),
                           ('VALIGN', (0,0), (0,0), 'MIDDLE'),
                           ('FONTSIZE', (0,0), (0,0), 24),
                           ('TEXTCOLOR', (0,0), (0,0), fg)]))
    w,h = t.wrapOn(c,0,0)
    t.drawOn(c, 1*inch, 10.5*inch)

    #keys: namedtuple("match", "startx, starty0, starty1, midy")
    match_coord = dict()

    startpoints = dict()
    MatchKey = namedtuple("match_key", "round, match_from_bottom")
#    MatchVal = namedtuple("match_val", "startx, starty0, starty1, midy")

    for round in range(1, rounds + 1):

        # draw the right number of participants in this round
        lines_in_this_round = 2**(rounds-round)

        # This is the y distance between lines in the same round
        y_height = y_height_first_round * 2**(round-1)

        # This is the starting offset for this round
        y_offset_this_round = math.floor(y_height_first_round/2) * 2**(round-1)

        x_start_this_round = ((round-1)  * x_width_per_round) + (0.5 * inch)

        for linenum in range(0, lines_in_this_round):
            x_left = int(x_global_offset + x_width_per_round * (round-1))
            x_right = int(x_left + x_width_per_round) 

            y = y_global_offset + y_offset_this_round+ (linenum * y_height) 

            c.line(x_left, y, x_right, y)

            if linenum %2 == 1:
                # The top one of a match
                c.line(x_right, y, x_right, y-y_height)
                # match_val = MatchVal(startx= x_left,
                #                      starty0 = y - y_offset_this_round,
                #                      starty1 = y,
                #                      midy = y - y_offset_this_round/2)
                
                match_val = {"startx": x_left,
                             "starty0": y - y_offset_this_round,
                             "starty1": y,
                             "midy": y - y_offset_this_round}

                match_coord[MatchKey(round, math.floor(linenum / 2))] = match_val

            startpoints[(round, linenum)] = (x_left, y)

    # third place bracket, same level as round 1 match 1


    third_place_x = x_global_offset + (x_width_per_round * (rounds - 2))
    third_place_y = y_global_offset
    c.line(third_place_x, third_place_y      ,
           third_place_x + x_width_per_round, third_place_y)
    c.line(third_place_x                     , third_place_y + y_height_first_round,
           third_place_x + x_width_per_round, third_place_y + y_height_first_round)
    
    # vertical
    c.line(third_place_x + x_width_per_round, third_place_y + y_height_first_round,
           third_place_x + x_width_per_round, third_place_y)
    
    # third place line
    c.line(third_place_x + x_width_per_round    , third_place_y + y_height_first_round / 2,
           third_place_x + 2 * x_width_per_round, third_place_y + y_height_first_round / 2)

    c.drawString(third_place_x + x_width_per_round + .25*inch, third_place_y + y_height_first_round / 2 - .25 * inch,
                 '3rd')
    
    c.drawString(startpoints[(rounds, 0)][0] + .25*inch, startpoints[(rounds, 0)][1] - .25 * inch,
                 '1st')
    
    match_coord[MatchKey(rounds, 0)] = {"startx": third_place_x,
                                        "starty0":  third_place_y,
                                        "starty1": third_place_y + y_height_first_round,
                                        "midy" : third_place_y + int(y_height_first_round/2)}
    # pp(match_coord)


    tt.create_place_table(c, 3.5*inch, 9.5*inch)
 
    # add teams
    # pp(startpoints)
    place_people(c, startpoints, people, match_coord)

def make_3rd_place_bracket(c):
    pass
