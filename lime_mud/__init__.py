import logging

logger = logging.getLogger(__name__)


def default_config():
    """Returns the default values for configuration parameters for this plugin

    The resulting configuration will be available under
    `lime_config.config['plugins']['lime_mud']`

    The values here can be overridden in the service's config file.
    """

    return {}


try:
    from .endpoints import register_blueprint  # noqa
except ImportError:
    logger.info('lime_mud doesn\'t implement any custom endpoints')

try:
    from .event_handlers import register_event_handlers  # noqa
except ImportError:
    logger.info('lime_mud doesn\'t implement any event handlers')

try:
    from .limeobject_classes import register_limeobject_classes  # noqa
except ImportError:
    logger.info('lime_mud doesn\'t implement any limeobject classes')
