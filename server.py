from flask import Flask, request
from flask_cors import CORS
from lib import config, log
from werkzeug.exceptions import HTTPException
from routes.roku import roku_template
from flask_swagger_ui import get_swaggerui_blueprint
from roku import Roku

try:
    c = config.Configuration('config.ini')
except Exception as e:
    exit()

fileLocation = None
log.setup_custom_logger(c.Logging.moduleName, c.Logging.level, fileLocation)
swaggerUiUrl = ''
swaggerDocUrl = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(swaggerUiUrl, swaggerDocUrl, config={'app_name': 'Roku API', 'validatorUrl': None, 'layout': 'BaseLayout'})

app = Flask(__name__, static_url_path="/static")
cors = CORS(app)

rokus = []
rokuSearch = {}
for rokuObj in c.Roku.hosts.split(','):
    rokuAttribs = rokuObj.split(':')
    rokus.append({'id': rokuAttribs[0], 'host': rokuAttribs[1]})
    rokuSearch[rokuAttribs[0]] = rokuAttribs[1]
app.rokus = rokus
app.rokuSearch = rokuSearch
app.Roku = Roku


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    if not hasattr(e, 'code'):
        return str(e), 500
    elif e.code > 499:
        app.logger.error(e)
    return e


app.register_blueprint(roku_template, url_prefix='/systems')
app.register_blueprint(swaggerui_blueprint, url_prefix=swaggerUiUrl)

if __name__ == '__main__':
    app.run(debug=False, threaded=True, host='0.0.0.0', port=8080)
