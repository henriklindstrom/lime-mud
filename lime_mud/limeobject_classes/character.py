import logging
from lime_type.limeobjects import LimeObject

logger = logging.getLogger(__name__)


class Character(LimeObject):
    """Summarize the function of a character object here"""

    def move(self, direction, uow):
        current_room = self.properties.location.fetch()
        exits = current_room.properties.exits.fetch()

        for exit in exits:
            if exit.properties.name.value == direction:
                next_room = exit.properties.to.fetch()
                char_idx = uow.add(self)
                self.properties.location.attach(next_room)
                uow.add(next_room)
                return char_idx

        raise NoSuchExitError(direction)


class NoSuchExitError(Exception):
    pass

def register_limeobject_classes(register_class):
    register_class('character',
                   Character)
