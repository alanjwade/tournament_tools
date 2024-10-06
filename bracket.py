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

MatchKey = namedtuple("match_key", "round, match_from_bottom")
def place_people(c, startpoints, people, match_coord):
    people_number = len(people)

    rounds = 5
    xy_offset = int(1/8 * inch)

    color_map = [
        ['#e6f7ff', '#cceeff', '#b3e6ff', '#99ddff', '#80d4ff', '#66ccff', '#4dc3ff', '#33bbff'],
        ['#e6fff2', '#ccffe6', '#b3ffd9', '#99ffcc'],
        ['#fff5e6', '#ffcc80'],
        ['#feeaea'],
        ['#feeaea']]
    

    
    people_log2_ceil = (people_number-1).bit_length()
    people_log2_floor = people_number.bit_length() - 1
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

    def write_match_num_str(c, round, match, use_offset=True):
        # x = match_coord[MatchKey(round=round, match_from_bottom=match)]['x_left']
        y_mid = match_coord[(round, match)]['y_mid']
        corner_x0 = match_coord[(round, match)]['x_left']
        corner_y0 = match_coord[(round, match)]['y_bottom']
        corner_y1 = match_coord[(round, match)]['y_top']
        corner_x1 = match_coord[(round, match)]['x_right']
        width = corner_x1 - corner_x0
        height = corner_y1 - corner_y0
        if 'populated_match_num' in match_coord[(round, match)]:
            match_num = match_coord[(round, match)]['populated_match_num']
        else:
            match_num = None
            

        ##############################
        # Fill in rectangles.
        ##############################
        if match_num:
            r,g,b = tt.hex_to_rgb(color_map[round-1][match])
            c.saveState()
            c.setFillColorRGB(r, g, b, 0.7)
            c.rect(corner_x0, corner_y0, width, height, fill=1, stroke = 0)
            c.restoreState()

        #############################
        # populate 'Match #x' for those indicated.
        #############################
        if match_num:
            c.saveState()
            c.setFont("Helvetica", 18)
            c.drawString(corner_x0 + xy_offset, y_mid, 'Match #{}'.format(match_num))
            c.restoreState()


        #############################
        # Fill in participants.
        #############################

        if 'top_part' in match_coord[(round, match)].keys():
            c.saveState()
            c.setFont("Helvetica", 12)
            if use_offset:
                x = corner_x0 + xy_offset
                y = corner_y1 + xy_offset
            else:
                x = corner_x0
                y = corner_y1

            c.drawString(x, y, match_coord[(round, match)]['top_part'])
            c.restoreState
        if 'bot_part' in match_coord[(round, match)].keys():
            c.saveState()
            if use_offset:
                x = corner_x0 + xy_offset
                y = corner_y0 + xy_offset
            else:
                x = corner_x0
                y = corner_y0

            c.drawString(x, y, match_coord[(round, match)]['bot_part'])
            c.restoreState

    def write_match_hint_str(c, round, match, win_lose_str, top_match, bot_match, use_offset=True):
        x = match_coord[(round, match)]['x_left']
        y_bot = match_coord[(round, match)]['y_bottom']
        y_top = match_coord[(round, match)]['y_top']
        c.saveState()
        c.setFillColor(colors.lightgrey)
        c.setFont("Helvetica", 12)
        if use_offset:
            x0 = x + xy_offset
            y0 = y_bot + xy_offset
            y1 = y_top + xy_offset
        else:
            x0 = x
            y0 = y_bot
            y1 = y_top
            
        c.drawString(x0, y0, win_lose_str + ' {}'.format(top_match))
        c.drawString(x0, y1, win_lose_str + ' {}'.format(bot_match))
        c.restoreState()

  


    # 0 based
    starting_participant_pos_in_second_round = total_participant_slots_in_second_round - num_people_second_round

    # Start with the participants in the second round, so the first person in
    # the people list is at the top.
    for part_pos in range(total_participant_slots_in_second_round - 1, \
                           total_participant_slots_in_second_round - 1 - num_people_second_round, \
                           -1):
    
        (x0, y0) = startpoints[(second_round, part_pos)]

        part_pos_int = math.floor(part_pos / 2)

        if part_pos %2 == 1:
            # This is the top one of a match
            match_coord[(second_round, part_pos_int)]['top_part'] =   people[people_pos]['Student First Name'] \
                                      + ' '  \
                                      + people[people_pos]['Student Last Name']  
        else:
            match_coord[(second_round, part_pos_int)]['bot_part'] =   people[people_pos]['Student First Name'] \
                                      + ' ' \
                                      + people[people_pos]['Student Last Name'] 
        #  c.drawString(x0 + xy_offset, y0 + xy_offset,   people[people_pos]['Student First Name'] 
        #                         + ' '
        #                         + people[people_pos]['Student Last Name'] )
        people_pos = people_pos + 1
        
    # Then go back a round and add the rest.
    # Here we'll discover what the first match is.
    for part_pos in range(num_people_first_round -1, \
                           -1, -1):
        (x0, y0) = startpoints[(starting_round, part_pos)]
        part_pos_int = math.floor(part_pos / 2)
        if part_pos %2 == 1:
            # This is the top one of a match
            match_coord[(starting_round, part_pos_int)]['top_part'] =   people[people_pos]['Student First Name'] \
                                      + ' '  \
                                      + people[people_pos]['Student Last Name']  
        else:
            match_coord[(starting_round, part_pos_int)]['bot_part'] =   people[people_pos]['Student First Name'] \
                                      + ' ' \
                                      + people[people_pos]['Student Last Name'] 
        # c.drawString(x0 + xy_offset, y0 + xy_offset,   people[people_pos]['Student First Name']
        #                      + ' '
        #                      + people[people_pos]['Student Last Name'])
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
            match_coord[(match_str_round, match_str_match)]['populated_match_num'] = match_num
            match_num += 1
    
    # Handle the third place match
    if len(people) > 2:
        match_coord[(rounds, 0)]['populated_match_num'] = match_num
      
        write_match_hint_str(c, rounds, 0,
                       'Loser Match', match_num - 2, match_num - 1)
        
        match_num += 1

    # Handle the first place match
    match_coord[(rounds-1, 0)]['populated_match_num'] = match_num
    # write_match_num_str(c, rounds-1, 0, match_num)
    if len(people) > 2:
        write_match_hint_str(c, rounds-1, 0,
                        'Winner Match', match_num - 3, match_num - 2)
        match_num += 1

    for round, match in match_coord.keys():
        write_match_num_str(c, round, match)



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
                
                match_val = {"x_left": x_left,
                             "x_right": x_right,
                             "y_bottom": y - y_height,
                             "y_top": y,
                             "y_mid": y - y_height/2}

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
    
    match_coord[MatchKey(rounds, 0)] = {"x_left": third_place_x,
                                        "x_right": third_place_x + x_width_per_round,
                                        "y_bottom":  third_place_y,
                                        "y_top": third_place_y + y_height_first_round,
                                        "y_mid" : third_place_y + int(y_height_first_round/2)}
    # pp(match_coord)


    tt.create_place_table(c, 3.5*inch, 9.5*inch)
 
    # add teams
    # pp(startpoints)
    place_people(c, startpoints, people, match_coord)

    tt.place_timestamp(c, 1/4*inch, 1/4*inch)

def make_3rd_place_bracket(c):
    pass
