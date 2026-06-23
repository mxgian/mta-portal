# MTA Portal

<img src="MTAPortal.jpg" alt="drawing" width="300"/>
This is a fork of https://github/com/alejandrorascovan/mta-portal which has not been updated in a number of years.  In order to make it work there are a few steps that must be completed first.  These are my recommendations, please proceed at your own risk.  

1) After physically installing the Adafruit Matrix M4 Hat to your pixel display, verify it works, it should have a default program (mine was the rotating pixel demo)
2) Update the firmware on the ESP32: https://learn.adafruit.com/upgrading-esp32-firmware/overview
3) In order to connect to wifi you will need to transition from a secrets.py file to a settings.toml (ignore any documentation that tells you to setup a secrets.py).  A sample settings.toml is included. 
4) The adafruit libraries that make the matrix rgb hat work required an adafruit IO login (i could not make it work without doing this) go to io.adafruit.com to sign-up.  A basic Adafruit IO account is free, but you will need to sign up and generate an API key.  Once you have those include your ID and API Key in the settings.toml
5) The included code is very basic as it only can handle 1 train line, and N / S directions.  In my case, my station has 2 train lines and therefore I need to filter out the train times for each line.  If your train station has multiple lines, you will need to do the same. 

Other Tips:
-The train times are sourced from the MTA however it relies on a JSON proxy (https://api.wheresthefuckingtrain.com/) which is run by a 3rd party without much documentation.  This itself is a fork of https://github.com/jonthornton/MTAPI, if you want to be safe consider deploying this proxy yourself on your local network.  
-Station IDs: There is a list of station IDs included, however it only includes the Lat/Long.  You can cross-reference the station names from the MTAPI project: https://github.com/jonthornton/MTAPI/blob/master/data/stations.csv You need to load the station-id statically at the top of the code.py
--I've included a screenshot example of all the libraries i've used, no guarantees that these are the minimum needed
--Mu Editor (https://codewith.mu/) is no longer maintained, but i found it very useful to edit my code.py since it can connect directly to the serial of the Matrix ESP32 device. 

Customizing the Display
-For a 128x64 display you will only have room for 2 rows.  the default code arranges it as northbound/southbound for the G train.  If you would like to alter this you will need to modify the code.py to extract the train times for the train and directions of your choosing, and then print them out on the appropriate row.  You will also need to create new bitmap logos for the associated trains.  
-The station names are hard-coded, update them with your's but keep in the mind the character limit (7 characters)
-I've included new bitmaps for my station, but two F trains as well as an F and G train.  These are loaded statically, pick the one you want to use or create your own using a pixel-editor

Practical Customized Example

For my board, my station is the 7Av station in Brooklyn for the F & G trains, this is station id F24.  As we only have 2 rows to work with the default is for the north and south trains, i wanted the northbound Queens trains for both the F & G, ignoring the southbound Brookyln/Coney Island trains.  I updated the code to filter out the train times for the F & G [remember this is required if you have more than one train line going to your station] trains into separate arrays and then i print out the times for the trains and directions i want.  

I made a crude frame for mine using 1/2 inch by 3 inch craft board, unfortunately Adafruit did not account for the placement of the hat--i think they wanted to provide easier access to the buttons, but it means it will stick out the side and you need to deal with it--or in my case don't deal with it.




# Previous Release Notes Below This Line
Run your own MTA Portal on CircuitPython to display trains arrivals using Adafruit's [hardware](https://www.adafruit.com/product/4812) and libraries.

Follow Adafruit main [tutorial](https://learn.adafruit.com/adafruit-matrixportal-m4) to set up your MatrixPortal.

## Config

You'll need your own `secrets.py`. Check [here](https://learn.adafruit.com/adafruit-matrixportal-m4/internet-connect) on how to create one.

Config variables:

- `STOP_ID`: Find your station ID [here](https://github.com/jonthornton/MTAPI/blob/master/data/stations.json)
- `UPDATE_DELAY`: Delay in seconds before fetching new data
- `MINIMUM_MINUTES_DISPLAY`: Only display arrival times greater or equal than this value. Useful to only show trains you can catch.
- `BACKGROUND_IMAGE`: Image to use for the background

## Installation

Just copy all the files into your CIRCUITPYTHON drive
