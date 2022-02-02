# Disclaimer

I don't take any responsibility for costs incurred using this image loader. The reality is that there is a 
call to an API, which has a cost, within a loop. 

**If this malfunctions for whatever reason and 
costs you more money than anticipated, I am not liable.**

I have attempted to put rudimentary safeguards in place however you are free to override these in 
the config.py. 

**If this safeguard fails or doesn't work as anticipated, I am not liable.**

If you are not comfortable accepting this risk, this is Licensed under an MIT license which effectively 
means you are free to dissect and take apart and use any part of this you wish. Feel free to use to 
code here to build your own tool and put inplace your own safeguards in place.

Quick summary of the MIT license is available [here](https://tldrlegal.com/license/mit-license)

I'm not liable if you use this tool to contravene the 
[Google Map Terms and Conditions](https://developers.google.com/maps/terms), please read and understand these before
using this tool

# Pricing

([Static Map Usage and Billing](https://developers.google.com/maps/documentation/maps-static/usage-and-billing))
Before setting this up, it is important to know this isn't free. Google Maps API has costs. At time 
of writing (please check above link for most up-to-date information) its around 2USD per 1000 images, 
a single image being 640x640.

That means that if you load a 700x700 image, for example, using this tool **you are actually paying 
for more than one image** (in this example, 4 images) as they will be stitched together to generate 
the size you want. Check out prices in the link above

# How to install
```pip install git+https://github.com/cormac-rynne/gmaploader.git```

# How to use
Most simplistic:

```python
import os
os.environ['GMAP_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

from gmaploader import GMapLoader

# Inputs
lat = 51.563839178
lon = -0.164794922

# Initalise
gml = GMapLoader(lat=lat, lon=lon)

# Image
img = gml.img
```

Other parameters:

```python
import os
os.environ['GMAP_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

from gmaploader import GMapLoader

# Inputs
lat = 51.563839178
lon = -0.164794922
width = 1200
height = 300
zoom = 16
map_type = 'satellite'

# Initalise
gml = GMapLoader(
    lat=lat,
    lon=lon,
    width=width,
    height=height,
    zoom=zoom,
    map_type=map_type
)

# Image
img = gml.img
```

# Useful links

* [Google Map Terms and Conditions](https://developers.google.com/maps/terms)
* [Google Maps Services Python Github](https://github.com/googlemaps/google-maps-services-python/)
* [Static Map Usage and Billing](https://developers.google.com/maps/documentation/maps-static/usage-and-billing)
* [Setup GCP account](https://cloud.google.com/apigee/docs/hybrid/v1.4/precog-gcpaccount)
* [Setting local environment variables](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html)
* [MIT License Quick Summary](https://tldrlegal.com/license/mit-license)

# Requirements

 - Python 3.5 or later.
 - A Google Maps API key.
 - matplotlib>=3.3.4
 - Pillow>=9.0.0

# Set your GCP Google Map API Key

## Where to get your key

* If you don't have a GCP account, there is a guide to do that 
[here](https://cloud.google.com/apigee/docs/hybrid/v1.4/precog-gcpaccount)
* If you already have one setup, go to https://console.cloud.google.com/
* In the Products menu on the left hand side, scroll down to 'Google Maps Platform'
* Click 'APIs' and enable 'Maps Static API'
* Then click 'credentials' and 'CREATE CREDENTIALS' at the top, then 'API Key'

## Restrict key

It is a good idea to add restrictions to the Key so it's less likely to be misused. To add a basic 
restriction (which restrict the use of the key to your IP address only), do the following:
* Then click 'Edit' on the API Key
* Click 'IP addresses'
* Go to https://whatismyipaddress.com/ and copy your IP address
* Paste your IP address into application restriction 
* Click 'Done' and 'Save'

More information on API security best practices [here](https://developers.google.com/maps/api-security-best-practices)


## Set key as environment variable

To save your key in an environment variable on your computer, you can use 
[this guide](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html) 
however you will need to close and restart Python after setting it to be able to use it. 
This tool looks for the key under 'GMAP_KEY', however you can change this in the config.py file


# Credits/Acknowledgements

* maptiler - [globalmaptiles.py](https://gist.github.com/maptiler/fddb5ce33ba995d5523de9afdf8ef118)
