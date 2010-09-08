"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    # TODO: append and redirect urls that don't end in a slash
    # Also: should I remove these convenience maps to prevent two URLs
    # from pointing to the same page?
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/')
    map.connect('/{controller}/{action}/{id}')

    map.connect('/', controller='main', action='index')

    map.connect('/game/', controller='game', action='index')
    map.connect('/game/new/ai/', controller='game', action='new_ai_choose')
    map.connect('/game/new/ai/{diff}/', controller='game', action='new_ai')
    map.connect('/game/new/versus/', controller='game', action='new_versus')
    map.connect('/game/cont/{id}/', controller='game', action='cont_game')
    map.connect('/game/cont/{id}/comet/', controller='game', action='long_poll')

    return map
