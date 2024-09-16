import re

LEVELS= ["Beginner", "Level 1", "Level 2", "Level 3", "Black Belt"],
PHYSRINGCOLORMAP= {
    1: "#ff0000", # red
    2: "#ffa500", # orange
    3: "#ffff00", # yellow
    4: "#34a853",
    5: "#0000ff",
    6: "#fd2670",
    7: "#8441be", # purpleish
    8: "#999999",
    9: "#000000", # black
    10: "#b68a46",
    11: "#f78db3",
    12: "#6fa8dc",
    13: "#b6d7a8",
    14: "#b4a7d6"
}
DISPLAYSTYLE= "sections" # physical rings (1,2,3... or 1a, 1b, 2a, 2b, ...)
                         # sections (ring 1 section 1, ring 1 section 2, etc.)

global get_ring_colors
def get_ring_colors(phys_ring_str):
    
    match = re.search(r'\d+', phys_ring_str)

    if match:
        bg_color = PHYSRINGCOLORMAP[int(match[0])]
        fg_color = "#000000" # black
        if bg_color in ["#000000", "#0000ff", "#8441be"]:
            fg_color = "#ffffff" # white
        return [fg_color, bg_color]
    else:
        return ["#000000", "#ffffff"]
def short_school_name(school_name):
    '''Abbreviate a school name.'''
    if 'Exclusive' in school_name:
        return 'EMA'
    elif 'Personal' in school_name:
        return 'PAMA'
    elif 'Success' in school_name:
        return 'SMA'
    elif '5280' in school_name:
        return '5280'
    elif 'Fort Collins' in school_name:
        return 'REMA FC'
    elif 'Longmont' in school_name:
        return 'REMA LM'
    elif 'Johnstown' in school_name:
        return 'REMA JT'
    elif 'Broomfield' in school_name:
        return 'REMA BF'
    else:
        return None

def ring_name_expanded(ring):
    '''Take physical ring 1-a and make 'Ring 1 Group A'.'''

    if '-' in ring:
        parts = ring.split('-')
        return 'Ring {} Group {}'.format(parts[0], parts[1].upper())
    else:
        return 'Ring {}'.format(ring)
