import re
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime
import pytz

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

def hex_to_rgb(hex_color):
  """Converts a hex color string to an RGB tuple.

  Args:
    hex_color: A string representing the hex color, e.g., "#FF00FF".

  Returns:
    An RGB tuple (r, g, b) where r, g, and b are integers in the range 0-255.
  """

  # Remove the '#' prefix if present
  if hex_color.startswith('#'):
    hex_color = hex_color[1:]

  # Ensure the hex color string is 6 characters long
  if len(hex_color) != 6:
    raise ValueError("Invalid hex color format: must be 6 characters long")

  # Convert each pair of characters to an integer
  r = int(hex_color[:2], 16)
  g = int(hex_color[2:4], 16)
  b = int(hex_color[4:], 16)

  return (r/255, g/255, b/255)

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
    

def create_place_table(c, x, y):
    '''Draw a place table.'''

    data = [['Final Place', 'Name'],
            ['1st', ''],
            ['2nd', ''],
            ['3rd', '']]
    
    t = Table(data, [1*inch, 3 * inch])
    t.setStyle(TableStyle([('ALIGN', (0,0), (-1, -1), 'RIGHT'),
                           ('ALIGN', (1,0), (1,0), 'CENTER'),
                           ('GRID', (-1, 1), (-1, -1), 2, colors.black)]))
    w,h = t.wrapOn(c, 0, 0)
    t.drawOn(c, x, y)



def create_timestamp_string():
  """Creates a timestamp string including date, hours, minutes, seconds, and timezone."""

  # Get the current time in UTC
  utc_time = datetime.datetime.utcnow()

  # Get the timezone of the current location
  timezone = pytz.timezone('America/Denver')  # Replace with your timezone

  # Convert the UTC time to the local timezone
  local_time = utc_time.astimezone(tz = timezone)

#  local_time = datetime.datetime.now()
  utc_dt = datetime.datetime.now(datetime.timezone.utc)
  dt = utc_dt.astimezone()

  # Format the timestamp string
  timestamp_string = 'Created ' + dt.strftime('%Y-%m-%d %H:%M:%S %Z')

  return timestamp_string

def place_timestamp(c, x, y):

    c.saveState()
    c.drawString(x, y, create_timestamp_string())
    c.restoreState()