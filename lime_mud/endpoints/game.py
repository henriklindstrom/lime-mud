import lime_webserver.webserver as webserver
import logging
import webargs.fields as fields
from webargs.flaskparser import use_args
from ..endpoints import api
import flask


logger = logging.getLogger(__name__)



class World(webserver.LimeResource):
    """Summarize your resource's functionality here"""

    def get(self):
        """Get a game
        """

        characters = self.application.limetypes.character.get_all()

        res = {
            'characters': []
        }

        for character in characters:
            location = character.properties.location.fetch()
            res['characters'].append(
                {
                    'name': character.properties.name.value,
                    'location': location.properties.name.value
                }
            )

        return res


move_args = {
    'exit': fields.Str(required=True)
}


class ActionMove(webserver.LimeResource):

    @use_args(move_args)
    def post(self, args):
        character = self.application.coworker

        try:
            uow = self.application.unit_of_work()
            char_idx = character.move(args.get('exit'), uow)
            res = uow.commit()
            character = res.get(char_idx)
            return character.properties.location.fetch().describe()
        except Exception:
            logger.exception('Error when moving')
            return {'error': 'you cannot go there'}, 400


class ActionLook(webserver.LimeResource):

    def get(self):
        character = self.application.coworker
        return character.properties.location.fetch().describe()


api.add_resource(World, '/world/')
api.add_resource(ActionMove, '/move/')
api.add_resource(ActionLook, '/look/')
