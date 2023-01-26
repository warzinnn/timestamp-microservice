"""
application factory
"""

import os  # import os to be able to access environment variables

from flask import Flask

from src.blueprints.api import blueprint_api


def create_app():
    app = Flask(__name__)

    # Config via os environment
    environment_configuration = os.getenv(
        "CONFIGURATION_SETUP", default="config.DevelopmentConfig"
    )
    app.config.from_object(environment_configuration)

    print(f"Environment: {app.config['ENV']}")
    print(f"Debug: {app.config['DEBUG']}")

    # Register blueprint
    app.register_blueprint(blueprint_api.blueprint_api, url_prefix="/api")

    return app
