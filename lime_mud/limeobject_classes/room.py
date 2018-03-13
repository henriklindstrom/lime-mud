import logging
from lime_type.limeobjects import LimeObject

logger = logging.getLogger(__name__)


class Room(LimeObject):
    """Summarize the function of a character object here"""

    def describe(self):
        exits = self.properties.exits.fetch()
        characters = self.properties.characters.fetch()
        items = self.properties.items.fetch()

        description = {
            'name': self.properties.name.value,
            'description': self.properties.description.value,
            'exits': [e.properties.name.value for e in exits],
            'characters': [c.properties.name.value for c in characters],
            'items': [i.properties.name.value for i in items]
        }
        
        return description


def register_limeobject_classes(register_class):
    register_class('room', Room)
