import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt


class Light(hass.Hass):

    def initialize(self):
        self.house_lights()

    def house_lights(self):
        # Call to Home Assistant to turn the porch light on
        # self.turn_on('light.backup_family_room_fan_light')
        pass