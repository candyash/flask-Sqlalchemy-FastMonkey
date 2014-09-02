from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.mail import Mail
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'fast.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    

    if not app.config['DEBUG'] and not app.config['TESTING'] and os.environ.get('HEROKU') is None:
     
        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .fast import fast as fast_blueprint
    app.register_blueprint(fast_blueprint)

    from .fastlog import fastlog as fastlog_blueprint
    app.register_blueprint(fastlog_blueprint, url_prefix='/fastlog')
    
    return app
   