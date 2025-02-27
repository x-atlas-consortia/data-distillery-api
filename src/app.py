from os import path
from flask import Flask
from pathlib import Path
from ubkg_api.app import UbkgAPI, logger


def make_flask_config():
    """
        Used to override the "native" app.cfg for the ubkg-api instantiated by the child API with
        values from the child API.
    """
    temp_flask_app = Flask(__name__,
                           instance_path=path.join(path.abspath(path.dirname(__file__)), 'data_distillery_api/instance'),
                           instance_relative_config=True)
    temp_flask_app.config.from_pyfile('app.cfg')
    return temp_flask_app.config


# Overwrite the ubkg-api's app configuration with the configuration from data-distillery-api.
cfg = make_flask_config()
app = UbkgAPI(cfg, Path(__file__).absolute().parent.parent).app
app.config = cfg


####################################################################################################
## For local development/testing
####################################################################################################

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port="5002")
    except Exception as e:
        print("Error during starting debug server.")
        print(str(e))
        logger.error(e, exc_info=True)
        print("Error during startup check the log file for further information")
