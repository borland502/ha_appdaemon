import appdaemon.plugins.hass.hassapi as hass


class OfflineCheck(hass.Hass):

    def initialize(self):
        self.log('Initializing Offline Check')

    def checkDevices(self):
        pass