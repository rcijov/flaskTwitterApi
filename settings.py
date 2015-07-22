#settings.py
import os
from twitter import *

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

APP_TWITTER = Twitter(consumer_key = 'SZOG9YyCPcT2fsfVt4AZ9aHUs',
        	      consumer_secret = 'naxVoame4wyGGsdFFIStfCe8HGP1n9HIA382RQxauIshOxCAW3',
        	      access_token = '168262562-Fc2GxGEOYJKSvOxqqlgGLUH1kUbaedKW3WmzfxcN',
        	      access_token_secret = 'aEdEUqYnlu3Yhb67uE8f5PFmIfpAOgqYwl9jEit6tg7gF')

