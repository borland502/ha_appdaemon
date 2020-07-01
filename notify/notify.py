import appdaemon.plugins.hass.hassapi as hass
import pychromecast
import time
import json
import socket
import os.path
from gtts import gTTS

#
# Notify
#
# Adapted for Appdaemon from https://github.com/GhostBassist/GooglePyNotify/blob/master/GooglePyNotify.py
#
# Args:
#

HOST_NAME = "192.168.2.6"
HOST_PORT = 80

MP3_CACHE_DIR = "mp3_cache"
ENDPOINT = 'notify'


class Notify(hass.Hass):

    def initialize(self):
        self.log("Initializing endpoint")
        self.register_endpoint(self.handle_request, "notify")

        self.log("Getting chromecasts...")
        # noinspection PyAttributeOutsideInit
        self.chromecasts = pychromecast.get_chromecasts()

        if not os.path.exists(MP3_CACHE_DIR):
            os.makedirs(MP3_CACHE_DIR)

    def handle_request(self, data):
        self.log(data)

        self.notify(str(data["message"]))

        return 200

    def notify(self, notification):
        if notification == "":
            notification = "No+Notification+Data+Received"

        mp3 = MP3_CACHE_DIR + "/" + notification.replace("+", "_") + ".mp3"
        text = notification.replace("+", " ")

        if not os.path.isfile(mp3):
            self.log("Generating MP3...")
            tts = gTTS(text=text,
                       lang='en-us')  # See Google TTS API for more Languages (Note: This may do translation Also - Needs Testing)
            tts.save(mp3)
        else:
            self.log("Reusing MP3...")

        self.log("Sending notification...")
        s = socket.socket(socket.AF_INET,
                          socket.SOCK_DGRAM)  # Pull IP Address for Local HTTP File Serving (Note: This requires an internet connection)
        s.connect(("192.168.2.3", 80))
        ip_add = s.getsockname()[0]
        self.log(ip_add)
        s.close()
        self.Cast(ip_add, mp3)

        self.log("Notification Sent.")

        return

    def Cast(self, ip_add, mp3):
        for cc in self.chromecasts:
            self.log(cc)
        castdevice = next(cc for cc in self.chromecasts[0] if cc.device.model_name == "Google Home" or
                          cc.device.model_name == "Google Home Mini" or cc.device.model_name == "Google Nest Hub")
        castdevice.wait()
        mediacontroller = castdevice.media_controller  # ChromeCast Specific
        url = "http://" + ip_add + "/" + mp3
        print(url)
        mediacontroller.play_media(url, 'audio/mp3')
        return

    def terminate(self):
        self.unregister_endpoint(self.handle_request)
