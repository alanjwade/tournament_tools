from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import math
from pprint import pprint as pp



def create_checkin_list(data, filename):
    """
    Creates a check-in list PDF using reportlab.ls
    Args:
        data (list): A list of dictionaries containing name, age, and school information.
        filename (str): The filename for the PDF output.
    """

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["Normal"]
    header_style = ParagraphStyle(name="Header", fontSize=12, bold=True)


    # Create the table header
    header_data = [["Name", "Age", "School"]]
    header_table = Table(header_data, style=[('ALIGN'    , (0, 0), (-1, 0), 'CENTER'),
                                             ('VALIGN'   , (0, 0), (-1, 0), 'MIDDLE'),
                                             ('FONTNAME' , (0, 0), (-1, 0), 'Helvetica-Bold'),
                                             ('FONTSIZE' , (0, 0), (-1, 0), 12)])

    # Create the table body
    body_data = header_data + [[person["name"], person["age"], person["school"]] for person in data]
    body_table = Table(body_data, [1 * inch, 0.5 * inch, 2 * inch], .25 * inch, repeatRows=1)

    body_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                    ('GRID', (0,1), (-1,-1), 2, colors.black)
                                   ]))

    # Create the PDF content
    elements = [
        Paragraph("Check-In List", title_style),
        # Spacer(10, 10),
        # header_table,
        Spacer(10, 10),
        body_table
    ]

    doc.build(elements)

def place_people(people):
    people_number = len(people)

    people_ceil = (people_number-1).bit_length()
    people_floor = people_number.bit_length() - 1

    print('{}:{}:{}'.format(people, people_ceil, people_floor))


def make_match(c, x_global_offset, y_global_offset, x_width_per_round, y_height_first_round, round, match):

    # Define the box
    x_left = x_global_offset + x_width_per_round * (round-1)
    x_right = x_left + x_width_per_round

    #            floor of the bracket  + initial y offset  * start of this one
    y_bottom = y_global_offset + (2**(round - 1) * y_height_first_round/2) + ((match -1) * 2**round * y_height_first_round)
    y_top = y_bottom + (2**(round - 1) * y_height_first_round)

    print('{}:{}:{}:{}'.format(x_left,y_bottom, x_right, y_top))
    c.line(x_left, y_bottom, x_right, y_bottom)
    c.line(x_right, y_bottom, x_right, y_top)
    c.line(x_left, y_top, x_right, y_top)

    # c.showPage()
    # c.save()
    # exit()
    return (x_left, y_bottom), (x_left, y_top)

def make_bracket2(c, teams):

    rounds = 5
    x_global_offset = 0.5 * inch
    y_global_offset = 0.5 * inch
    x_width_per_round = 1.5 * inch
    y_height_first_round = 0.6 * inch

    for round in range(1, rounds + 1):
        if round > 0:
            matches_in_this_round = int(2**(4-round))
        else:
            matches_in_this_round = int(0)


        y_height = 1/(2**round) * inch
        x_width = 1.5 * inch
        x_offset_per_round = 1.5
        x_start_this_round = ((round-1)  * x_offset_per_round * inch) + (0.5 * inch)


        for match in range(1, matches_in_this_round+1):
            x_start_this_round = ((round-1) * x_offset_per_round * inch) + (0.5 * inch)
            x_mid_this_round = x_start_this_round + x_offset_per_round/2
            y_mid_this_match = (0.5 * inch) + (match * y_height * 2)
            make_match(c, x_global_offset, y_global_offset, x_width_per_round, y_height_first_round, round, match)

def make_bracket(c, teams):
    '''given a canvas, make a bracket'''


    rounds = 5

    for round in range(1, rounds+1):

        if round > 0:
            matches_in_this_round = int(2**(4-round))
        else:
            matches_in_this_round = int(0)

        x_offset_per_round = 1.5
        y_offset_inside_matches = 24
        y_offset_between_matches = 1.0 * inch # for round 1

        # round in (1,5)
        x = ((round-1)  * x_offset_per_round * inch) + (0.5 * inch)
        y_offset = 2**(round-1) * 0.5 * inch
        for match in range(1, matches_in_this_round+1):
            # matches in (1,8) for round 1
            y_distance = 2**(round-1) * y_offset_between_matches
            y = ((match-1) * y_distance) + y_offset

            pp('{}:{}'.format(x,y))

            c.line(x, y, x + 100, y)
            c.line(x, y+y_offset_inside_matches, x + 100, y+y_offset_inside_matches)

def generate_tournament_bracket(teams, doc_name="tournament_bracket.pdf"):
    """Generates a 5-round tournament bracket with a 3rd place match.

    Args:
        teams: A list of team names.
        doc_name: The name of the output PDF file.
    """

    # Create a new PDF document
    doc = SimpleDocTemplate(doc_name, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    bracket_style = styles["Normal"]
    match_style = styles["Normal"]
    winner_style = match_style

    # Calculate the required number of rounds
    num_rounds = int(math.ceil(math.log2(len(teams))))

    # Create the bracket structure
    bracket = []
    for round_num in range(num_rounds):
        round_matches = []
        for match_num in range(2 ** round_num):
            match_data = [
                Paragraph(f"Team {match_num * 2 + 1}", bracket_style),
                Paragraph(f"Team {match_num * 2 + 2}", bracket_style),
                Paragraph("", match_style)  # Placeholder for winner
            ]
            round_matches.append(match_data)
        bracket.append(round_matches)

    # Add the 3rd place match
    third_place_match = [
        [Paragraph("Loser of Round {0} Match {1}".format(num_rounds - 1, 1), bracket_style)],
        [Paragraph("Loser of Round {0} Match {1}".format(num_rounds - 1, 2), bracket_style)],
        [Paragraph("", match_style)]  # Placeholder for 3rd place winner
    ]
    bracket.append(third_place_match)

    # Create the final bracket table
    table_data = []
    for round_matches in bracket:
        table_data.append([Paragraph(f"Round {bracket.index(round_matches) + 1}", header_style)] + round_matches)
    bracket_table = Table(table_data, colWidths=[100] + [150] * 3)

    # Add the bracket to the document
    doc.build([bracket_table])

# Sample data
data = [
    {"name": "Alice", "age": 18, "school": "High School A"},
    {"name": "Bob", "age": 17, "school": "High School B"},
    {"name": "Charlie", "age": 19, "school": "College C"}
]

data = data * 40

# Create the check-in list PDF
create_checkin_list(data, "checkin_list.pdf")




if __name__ == "__main__":
    teams = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]

    c = canvas.Canvas("bracket.pdf")
    make_bracket2(c, teams)

    place_people(['a'] * 7)

    c.showPage()
    c.save()