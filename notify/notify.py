import appdaemon.plugins.hass.hassapi as hass
import os.path
import pychromecast
from gtts import gTTS
from simhash import Simhash

#
# Notify
#
# Adapted for Appdaemon from https://github.com/GhostBassist/GooglePyNotify/blob/master/GooglePyNotify.py
#
# Args:
#

HOST_NAME = "192.168.2.6"
HOST_PORT = 8123

ENDPOINT_MSG = "notify"
BROADCAST_GRP = "Home group"

DOCKER_CONFIG_DIR = "/config"


class Notify(hass.Hass):

    def initialize(self):
        self.log("Initializing endpoint")
        self.register_endpoint(self.handle_request, "notify")

        if not os.path.exists(DOCKER_CONFIG_DIR + "/www/audio/appdaemon"):
            os.makedirs(DOCKER_CONFIG_DIR + "/www/audio/appdaemon")

    def handle_request(self, data):
        self.log(data)

        self.notify(str(data["message"]))

        return 200

    def notify(self, notification):
        if notification == "":
            notification = "No+Notification+Data+Received"

        mp3 = DOCKER_CONFIG_DIR + "/www/audio/appdaemon/" + str(Simhash(notification).value) + ".mp3"
        mp3_url = "http://" + HOST_NAME + ":" + str(HOST_PORT) + "/local/audio/appdaemon/" + str(Simhash(notification).value) + ".mp3"
        self.log(mp3)
        self.log(mp3_url)
        text = notification.replace("+", " ")

        if not os.path.isfile(mp3):
            self.log("Generating MP3...")
            tts = gTTS(text=text,
                       lang='en-us')  # See Google TTS API for more Languages (Note: This may do translation Also - Needs Testing)
            tts.save(mp3)
        else:
            self.log("Reusing MP3...")

        self.Cast(mp3_url)

        self.log("Notification Sent.")

    def Cast(self, mp3_url):

        casts, browser = pychromecast.get_listed_chromecasts(friendly_names=[BROADCAST_GRP])
        # Shut down discovery as we don't care about updates
        pychromecast.discovery.stop_discovery(browser)

        if len(casts) == 0:
            self.log("No Devices Found")

        cast = casts[0]
        cast.wait()

        mc = cast.media_controller
        mc.play_media(mp3_url, "audio/mp3")
        mc.block_until_active()

    def terminate(self):
        self.unregister_endpoint(self.handle_request)
