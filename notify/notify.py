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
class Notify(hass.Hass):

    def initialize(self):
        self.log(f"Initializing Notify endpoint with args {self.args}")
        self.register_endpoint(self.handle_request, self.args['endpoint'])

        if not os.path.exists(self.args['tts_cache_dir']):
            os.makedirs(self.args['tts_cache_dir'])

    def handle_request(self, data):
        self.log(data)

        self.notify(str(data['message']))

        return None, 200

    def notify(self, notification):
        if notification == '':
            notification = 'No+Notification+Data+Received'

        mp3_file_hash = str(Simhash(notification).value)
        mp3 = f"{self.args['tts_cache_dir']}/{mp3_file_hash}.mp3"
        mp3_url = f"http://{self.args['host_name']}{self.args['tts_www_dir']}/{mp3_file_hash}.mp3"
        self.log(mp3)
        self.log(mp3_url)
        text = notification.replace("+", " ")

        if not os.path.isfile(mp3):
            self.log('Generating MP3...')
            tts = gTTS(text=text,
                       lang='en-us')
            # save mp3 file to the HA config directory
            tts.save(mp3)
        else:
            self.log('Reusing MP3...')

        self.cast(mp3_url)

        self.log('Notification Sent.')

    def cast(self, mp3):

        casts, browser = pychromecast.get_listed_chromecasts(friendly_names=[self.args['broadcast_grp']])
        # Shut down discovery as we don't care about updates
        pychromecast.discovery.stop_discovery(browser)

        if len(casts) == 0:
            self.log('No Devices Found')

        cast = casts[0]
        cast.wait()

        mc = cast.media_controller
        mc.play_media(mp3, 'audio/mp3')
        mc.block_until_active()

    def terminate(self):
        self.unregister_endpoint(self.handle_request)
