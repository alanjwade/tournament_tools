# name tags
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
import tt_global

name_tag_width = (3.375 + 3/8) * inch
name_tag_height = (2 + 1/3 + .25) * inch
image_width = 0.75 * inch
image_height = 0.75 * inch

def create_name_tag(first_name, last_name, school, level, ring, ring_colors, image_path):
   

    styles = dict()

    styles['name'] = ParagraphStyle("name", None)
    styles['school'] = ParagraphStyle("school", None)
    styles['level'] = ParagraphStyle("level", fontName='Helvetica', fontSize=24)
    styles['ring'] = ParagraphStyle("ring",
                     fontName='Helvetica', 
                     fontSize=24,
                     textColor=ring_colors[0])
    
    table_data = [
        [Paragraph(first_name + ' ' + last_name, styles['level'])],
        [Paragraph(tt_global.short_school_name(school), styles['level'])],
        [Paragraph(level, styles['level']), Image(image_path, width=image_width, height=image_height)],
        [Paragraph(tt_global.ring_name_expanded(ring), styles['ring'])]
        ]

    table = Table(table_data, colWidths=[name_tag_width - image_width * 1.5, image_width],
                              rowHeights=[name_tag_height/6] * 4)
                              # rowHeight: make first on a little smaller
                              # so background has a big more space
    table.setStyle(TableStyle([
        ('TOPPADDING',    (0,0), (-1, -1), 0),
        ('BOTTOMPADDING', (0,0), (-1, -1), 0),
        ('LEFTPADDING',   (0,0), (-1, -1), 6),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        # ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('BOX', (0, 0), (-1, -1), 0.25, 'white'),
        ('BACKGROUND', (0,3), (0,3), ring_colors[1])
    ]))

    return table


def create_name_tags(filename, people, level, virt_to_phys_map):

    doc = SimpleDocTemplate(filename, pagesize=letter, 
                                      topMargin=((11 - 4*name_tag_height/inch)/2) * inch,
                                      bottomMargin = 0,
                                      leftMargin = 0,
                                      rightMargin = 0)
    elements = [[]]


    for person in people:

        # want a 2xvar array
        if len(elements[-1]) == 2:
            # add a new one
            elements.append([])

        ring = virt_to_phys_map[person['Virtual Ring']]
        ring_colors = tt_global.get_ring_colors(ring)

        elements[-1].append(create_name_tag(person['Student First Name'],
                                        person['Student Last Name'],
                                        person['School'],
                                        level,
                                        ring,
                                        ring_colors,
                                        "logo_orig_dark_letters.png"))
        

    #Add the name tags to the document in a 2x4 grid
    table_of_name_tags = Table(elements, colWidths=[name_tag_width, name_tag_width],
    rowHeights = [name_tag_height] * len(elements))
    table_of_name_tags.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('BOX', (0, 0), (-1, -1), 0.25, 'black')
    ]))

    # elements.append(table_of_name_tags)

    doc.build([table_of_name_tags])