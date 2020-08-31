import appdaemon.plugins.hass.hassapi as hass


class Info(hass.Hass):

    def initialize(self):
        self.log('Initializing Info')

    def get_entities_in_group(self, group):
        group = self.get_state(group, attribute="all")
        return group

    def check_group(self, entity, group):
        group = self.get_entities_in_group(group)
        return entity in group["attributes"]["entity_id"]
