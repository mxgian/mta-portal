import time
import microcontroller
from board import NEOPIXEL
import displayio
import adafruit_display_text.label
from adafruit_datetime import datetime
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrix import Matrix
from adafruit_matrixportal.network import Network

STOP_ID = 'F24'
DATA_SOURCE = 'https://api.wheresthefuckingtrain.com/by-id/%s' % (STOP_ID,)
DATA_LOCATION = ["data"]
UPDATE_DELAY = 15
SYNC_TIME_DELAY = 30
MINIMUM_MINUTES_DISPLAY = 5
BACKGROUND_IMAGE = 'f-g-dashboard.bmp'
ERROR_RESET_THRESHOLD = 3

def get_arrival_in_minutes_from_now(now, date_str):
    train_date = datetime.fromisoformat(date_str).replace(tzinfo=None) # Remove tzinfo to be able to diff dates
    return round((train_date-now).total_seconds()/60.0)

def get_arrival_times():
    stop_trains = network.fetch_data(DATA_SOURCE, json_path=(DATA_LOCATION,))
    stop_data = stop_trains[0]
#    nortbound_trains = [x['time'] for x in stop_data['N']]
    f_northbound_trains = []
    for x in stop_data['N']: 
        if x['route'] == 'F':
            #print ("xNroute", x['route'])
            f_northbound_trains.append(x['time']) 
        #print("N", x)
    g_northbound_trains = []
    for x in stop_data['N']: 
        if x['route'] == 'G':
            #print ("xNroute", x['route'])
            g_northbound_trains.append(x['time']) 
        #print("N", x)    
        
        
        
#   southbound_trains = [x['time'] for x in stop_data['S']]
    f_southbound_trains = []
    for x in stop_data['S']: 
        if x['route'] == 'F':
            f_southbound_trains.append(x['time']) 
            #print ("xSroute", x['time'])
            # print("S", x)
    g_southbound_trains = []
    for x in stop_data['S']: 
        if x['route'] == 'G':
            g_southbound_trains.append(x['time']) 
            #print ("xSroute", x['time'])
            # print("S", x)
    #route = [x['route'] for x in stop_data['N']]
    #print("train data", route)
    now = datetime.now()
    print("Now: ", now)

    #    nortbound_arrivals = [get_arrival_in_minutes_from_now(now, x) for x in nortbound_trains]
    #  the nortbound and southbound_arrivals only have the train times in them, which train times are determined by the for loops
    #above that filter on which train.  the two approaches below do the same thing, just testing out format
    # too lazy to rewrite next section, but northbound is row 1 of panel, and southbound is row 2
  
    northbound_trains = f_northbound_trains
    northbound_arrivals = []
    northbound_arrivals = [get_arrival_in_minutes_from_now(now, x) for x in northbound_trains]

    #for x in northbound_trains:
        #print ("X", x)
        #nortbound_arrivals.append(get_arrival_in_minutes_from_now(now, x))

    southbound_trains = g_northbound_trains
    southbound_arrivals = [get_arrival_in_minutes_from_now(now, x) for x in southbound_trains]

    n = [str(x) for x in northbound_arrivals if x>= MINIMUM_MINUTES_DISPLAY]
    s = [str(x) for x in southbound_arrivals if x>= MINIMUM_MINUTES_DISPLAY]

    n0 = n[0] if len(n) > 0 else '-'
    n1 = n[1] if len(n) > 1 else '-'
    s0 = s[0] if len(s) > 0 else '-'
    s1 = s[1] if len(s) > 1 else '-'

    return n0,n1,s0,s1

def update_text(n0, n1, s0, s1):
    text_lines[2].text = "%s,%s m" % (n0,n1)
    text_lines[4].text = "%s,%s m" % (s0,s1)
 #   display.show(group)
    display.root_group = group

# --- Display setup ---
matrix = Matrix()
display = matrix.display
network = Network(status_neopixel=NEOPIXEL, debug=False)

# --- Drawing setup ---
group = displayio.Group()
bitmap = displayio.OnDiskBitmap(open(BACKGROUND_IMAGE, 'rb'))
colors = [0x444444, 0xDD8000]  # [dim white, gold]

font = bitmap_font.load_font("fonts/6x10.bdf")
text_lines = [
    displayio.TileGrid(bitmap, pixel_shader=getattr(bitmap, 'pixel_shader', displayio.ColorConverter())),
    adafruit_display_text.label.Label(font, color=colors[0], x=20, y=3, text="Jamaica"),
    adafruit_display_text.label.Label(font, color=colors[1], x=20, y=11, text="- mins"),
    adafruit_display_text.label.Label(font, color=colors[0], x=20, y=20, text="Court"),
    adafruit_display_text.label.Label(font, color=colors[1], x=20, y=28, text="- mins"),
]
for x in text_lines:
    group.append(x)
#display.show(group)
display.root_group = group


error_counter = 0
last_time_sync = None
# Define your boundary times

#start_time = datetime.time('06:00')    # 09:00 AM
#end_time = datetime.time(23)    # 11:00 PM

# Get the current time of day
#current_time = datetime.now().time()
#print (current_time)   
#if start_time <= current_time <= end_time:
#    print("The current time is within business hours.")
#else:
#0    print("The office is closed.")

while True:
    try:
        if last_time_sync is None or time.monotonic() > last_time_sync + SYNC_TIME_DELAY:
            # Sync clock to minimize time drift
            network.get_local_time()
            last_time_sync = time.monotonic()
        arrivals = get_arrival_times()
        update_text(*arrivals)
    except (ValueError, RuntimeError) as e:
        print("Some error occured, retrying! -", e)
        error_counter = error_counter + 1
        if error_counter > ERROR_RESET_THRESHOLD:
            microcontroller.reset()

    time.sleep(UPDATE_DELAY)