# MTA Portal

<img src="MTAPortal.jpg" alt="drawing" width="300"/>
This is a fork of https://github/com/alejandrorascovan/mta-portal which has not been updated in a number of years.  In order to make it work there are a few steps that must be completed first.  These are my recommendations, please proceed at your own risk.  

1) After physically installing the Adafruit Matrix M4 Hat to your pixel display, verify it works, it should have a default program (mine was the rotating pixel demo)
2) Update the firmware on the ESP32: https://learn.adafruit.com/upgrading-esp32-firmware/overview
3) In order to connect to wifi you will need to transition from a secrets.py file to a settings.toml (ignore any documentation that tells you to setup a secrets.py).  A sample settings.toml is included. 
4) The adafruit libraries that make the matrix rgb hat work required an adafruit IO login (i could not make it work without doing this).  A basic Adafruit IO account is free, but you will need to sign up and generate an API key.  Once you have those include them in the settings.toml
5) The included code is very basic as it only can handle 1 train line, and N / S directions.  In my case, my station has 2 train lines and therefore I need to filter out the train times for each line.  If your train station has multiple lines, you will need to do the same. 

Other Tips:
-Station IDs: 



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
