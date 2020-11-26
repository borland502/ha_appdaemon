import appdaemon.plugins.hass.hassapi as hass


class LumenActivatedLights(hass.Hass):

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        self.sensor = self.args['sensor']
        self.threshold = self.args['threshold']
        self.entity = self.args['entity']

        self.run_minutely(self.check_lumen, None)

        # TODO timeout value if no motion is detected

    def check_lumen(self, kwargs):

        # activate lights only during dim parts of the day / evening
        if not self.now_is_between("11:00:00", "23:29:00"):
            return

        sensor_state = int(self.get_state(self.sensor))
        self.log(f"{self.sensor} is at {sensor_state}")

        self.notify(f"{self.sensor} is at {sensor_state}", title='appdaemon: illumination', name='pushbullet')

        # if the light exceeds the illumination threshold, then turn off.  Otherwise, turn on
        if self.get_state(self.entity) == "on":
            if sensor_state > self.threshold:
                self.turn_off(self.entity)
        else:
            if sensor_state < self.threshold:
                self.turn_on(self.entity)
