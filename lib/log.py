from logging.config import dictConfig


def setup_custom_logger(name, loggingLevel, fileLocation=None):
    logConfig = {
        'version': 1,
        'name': 'com.wwtatc.ad-api',
        'formatters': {'default': {
            'format': '%(asctime)s - %(levelname)s - '+name+' - %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }},
        'root': {
            'level': loggingLevel,
            'handlers': ['wsgi']
        }
    }
    if fileLocation:
        logConfig['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': fileLocation
        }
        logConfig['root']['handlers'].append('file')
    dictConfig(logConfig)
