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

    # pp(data)

    # Create the table header
    header_data = [["First Nmae", "Last Name", "School", "Forms?", "Sparring?", "Ring"]]
    header_table = Table(header_data, style=[('ALIGN'    , (0, 0), (-1, 0), 'CENTER'),
                                             ('VALIGN'   , (0, 0), (-1, 0), 'MIDDLE'),
                                             ('FONTNAME' , (0, 0), (-1, 0), 'Helvetica-Bold'),
                                             ('FONTSIZE' , (0, 0), (-1, 0), 12)])

    # Create the table body
    body_data = header_data + [[person["Student First Name"], person["Student Last Name"], person["School"],
                                person["Form"], person["Sparring"], person["Virtual Ring"]] for person in data]
    body_table = Table(body_data, [1 * inch, 2 * inch, 0.75 * inch, .5 * inch, .5*inch, .5 * inch], repeatRows=1)

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

def make_bracket(c, teams):
    '''given a canvas, make a bracket'''

    c.line(0, 0, 200, 300)


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
# data = [
#     {"name": "Alice", "age": 18, "school": "High School A"},
#     {"name": "Bob", "age": 17, "school": "High School B"},
#     {"name": "Charlie", "age": 19, "school": "College C"}
# ]

# data = data * 40

# # Create the check-in list PDF
# create_checkin_list(data, "checkin_list.pdf")




if __name__ == "__main__":
    teams = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]

    c = canvas.Canvas("bracket.pdf")
    make_bracket(c, teams)

    c.showPage()
    c.save()