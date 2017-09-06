import argparse
# Add trashtalk to the sys.path for loading
import sys
from trashtalk.factories import app_factory

parser = argparse.ArgumentParser("Trashtalk", description="A demonstration.")
parser.add_argument('-t', '--test',
                    action='store_true',
                    dest='test',
                    help='Set server mode to test.')
parser.add_argument('-p', '--prod',
                    action='store_true',
                    dest='production',
                    help='Set server mode to production.')

settings = parser.parse_args()


if __name__ == '__main__':
    if settings.test:
        app = app_factory('trashtalk.settings.Testing')
        app.logger.info("Test server configured...")
    elif settings.production:
        app = app_factory('trashtalk.settings.Production')
        app.logger.info("Production server configured ...")
    else:
        app = app_factory('trashtalk.settings.Development')
        # app.config.from_pyfile('dev.cfg')
        app.logger.info('Welcome to the Development server')

    app.run()

