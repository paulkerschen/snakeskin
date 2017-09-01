import logging
from logging.handlers import RotatingFileHandler


def initialize_logger(app):
    handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], mode='a', maxBytes=1024 * 1024 * 100, backupCount=20)
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
