import os.path

import appdaemon.plugins.hass.hassapi as hass
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

    async def initialize(self):
        self.casts, self.browser = pychromecast.get_chromecasts()

        await self.register_endpoint(self.handle_request, self.args['endpoint'])

        if not os.path.exists(self.args['tts_cache_dir']):
            os.makedirs(self.args['tts_cache_dir'])

    async def handle_request(self, data):
        uuid = data.setdefault('uuid', None)
        await self.notify(str(data['message']), uuid)

        return None, 200

    async def notify(self, notification=None, target_speaker=None):
        if notification is None:
            notification = 'No+Notification+Data+Received'

        if target_speaker is None:
            target_speaker = self.args['broadcast_grp']

        mp3_file_hash = str(Simhash(notification).value)
        mp3 = f"{self.args['tts_cache_dir']}/{mp3_file_hash}.mp3"
        mp3_url = f"http://{self.args['host_name']}{self.args['tts_www_dir']}/{mp3_file_hash}.mp3"

        text = notification.replace("+", " ")

        if not os.path.isfile(mp3):
            self.log('Generating MP3...')
            tts = gTTS(text=text,
                       lang='en-us')
            # save mp3 file to the HA config directory
            tts.save(mp3)
        else:
            self.log('Reusing MP3...')

        await self.cast(mp3_url, target_speaker)

        self.log('Notification Sent.')

    async def cast(self, mp3, target_speaker):

        if len(self.casts) == 0:
            self.log('No Devices Found')

        for cast in self.casts:
            if str(cast.uuid) == target_speaker:
                cast.wait()

                mc = cast.media_controller
                mc.play_media(mp3, 'audio/mp3')
                mc.block_until_active()
                break

    def terminate(self):
        self.unregister_endpoint(self.handle_request)
        pychromecast.discovery.stop_discovery(self.browser)
        self.casts = None
        self.browser = None
