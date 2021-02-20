import datetime

import appdaemon.plugins.hass.hassapi as hass
from distutils import util


class ClosedCheck(hass.Hass):
    def initialize(self):
        self.log('Initializing Closed Check')

        time = datetime.time(20, 0, 0)
        self.run_daily(self.check_entities, time)
        # self.run_minutely(self.check_entities, None)

    def check_entities(self, kwargs):

        garage_msg = "Garage is open"

        for entity in self.args['entities']:
            if util.strtobool(f"{self.get_state(entity)}"):
                if entity == 'binary_sensor.door_window_sensor_158d000632c277':
                    self.notify(garage_msg, name='cq')
                    self.notify(garage_msg, name='kitchen_display')
                    self.notify(garage_msg, name='hallway')


class OfflineCheck(hass.Hass):

    def initialize(self):
        self.log('Initializing Offline Check')

    def checkDevices(self):
        pass
