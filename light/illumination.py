import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime


class MotionActivatedLights(hass.Hass):

    def initialize(self):
        self.log('Initialize Dining Room Sensor')

        self.sensor = self.args['sensor']
        self.threshold = self.args['threshold']
        self.entity = self.args['entity']
        self.event_name = self.args['event_name']
        self.event_entity = self.args['event_entity']

        self.listen_event(self.check_lumen, self.event_name)

        # TODO timeout value if no motion is detected

    def check_lumen(self, event_name, data, kwargs):

        # Motion activate lights only during dim parts of the day / evening
        if self.sun_down():
            return

        # We are only interested in one sensor out of many for a motion/illumination event
        if data['entity_id'] != self.event_entity:
            return

        sensor_state = int(self.get_state(self.sensor))

        # if the light exceeds the illumination threshold, then turn off.  Otherwise, turn on
        if self.get_state(self.entity) == "on":
            if sensor_state > self.threshold:
                self.turn_off(self.entity)
        else:
            if sensor_state < self.threshold:
                self.turn_on(self.entity)
