import appdaemon.plugins.hass.hassapi as hass
from ping3 import ping


class Backup(hass.Hass):

    def initialize(self):
        pass
        # self.log('initializing backup script')
        # self.notify('initializing backup script', title='appdaemon: Backup', name='pushbullet')
        # self.run_every(self.check_primary, "now", 5 * 60)

    def check_primary(self, kwargs):
        pass
        # try:
        #     primary_host = ping('192.168.2.13')
        #     self.log(f"primary host response time: {primary_host}")

        #     # check if the primary home assistant is up.  If not, restart it
        #     if not primary_host:
        #         self.log('Home assistant is down')

        #         # don't wake us up in the middle of night, or the kids
        #         if not self.now_is_between("00:00:00", "09:00:00"):
        #             return

        #         # noinspection PyUnresolvedReferences
        #         # self.get_app('notify').notify('Home assistant is down', self.args['speaker'])
        #         self.notify('initializing backup script', title='appdaemon: Backup', name='pushbullet')

        #         # self.turn_off('switch.home_assistant')

        #         # self.turn_on('switch.home_assistant')
        # except Exception as ex:
        #     print(ex)

    def terminate(self):
        self.log('Terminating Backup App')
