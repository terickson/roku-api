import json
from flask import Blueprint, current_app, Response, request
from pprint import pprint
from time import sleep

roku_template = Blueprint('roku_template', __name__, template_folder='templates')


@roku_template.route('/', methods=['GET'])
def systems():
    return list()


@roku_template.route('/<string:id>', methods=['GET'])
def system(id):
    return show(id)


@roku_template.route('/<string:id>/actions', methods=['POST'])
def actions(id):
    return create_action(id)


def list():
    return Response(json.dumps(current_app.rokus), mimetype='application/json')


def show(id):
    current_app.logger.info("get roku " + id)
    if id not in current_app.rokuSearch:
        return Response(status=404)
    rokuReturn = {'id': id, 'host': current_app.rokuSearch[id], 'apps':[]}
    roku = current_app.Roku(current_app.rokuSearch[id])
    for app in roku.apps:
        rokuReturn['apps'].append({'id': app.id, 'name': app.name})
    pprint(rokuReturn['apps'])
    return Response(json.dumps(rokuReturn), mimetype='application/json')


def create_action(id):
    current_app.logger.info("post roku action for: " + id)
    if id not in current_app.rokuSearch:
        return Response(status=404)
    roku = current_app.Roku(current_app.rokuSearch[id])
    action = request.get_json(force=True)
    current_app.logger.info("action: " + str(action))
    if 'command' not in action:
        return Response(json.dumps({"message": "command must be supplied"}), status=412, mimetype='application/json')
    commandUpper = action['command'].upper()
    if commandUpper == 'HOME':
        roku.home()
    elif commandUpper == 'BACK':
        roku.back()
    elif commandUpper == 'UP':
        spaces = int(action['value'])
        runRokuCommandXTimes(roku, spaces, 'up')
    elif commandUpper == 'DOWN':
        spaces = int(action['value'])
        runRokuCommandXTimes(roku, spaces, 'down')
    elif commandUpper == 'LEFT':
        spaces = int(action['value'])
        runRokuCommandXTimes(roku, spaces, 'left')
    elif commandUpper == 'RIGHT':
        spaces = int(action['value'])
        runRokuCommandXTimes(roku, spaces, 'right')
    elif commandUpper == 'ENTER':
        roku.enter()
    elif commandUpper == 'SELECT':
        roku.select()
    elif commandUpper == 'PLAY':
        roku.play()
    elif commandUpper == 'PAUSE':
        roku.play()
    elif commandUpper == 'FORWARD':
        roku.forward()
    elif commandUpper == 'REVERSE':
        roku.reverse()
    elif commandUpper == 'SEARCH':
        searchTerm = action['value'].lower()
        roku.search()
        roku.literal(searchTerm)
    elif commandUpper == 'INPUT':
        app = roku[action['value']]
        app.launch()
    else:
        return Response(json.dumps({"message": "Action command " + commandUpper + " could not be found."}), status=412, mimetype='application/json')

    return Response(json.dumps({"message": "success"}), status=201, mimetype='application/json')


def runRokuCommandXTimes(roku, x, value):
    for i in range(x):
        getattr(roku, value)()
        sleep(1)
