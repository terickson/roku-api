import json
from flask import Blueprint, current_app, Response, request
from pprint import pprint
from time import sleep

roku_template = Blueprint('roku_template', __name__, template_folder='templates')


@roku_template.route('/', methods=['GET'])
def users():
    return list()


@roku_template.route('/<string:id>', methods=['GET'])
def user(id):
    return show(id)


@roku_template.route('/<string:id>/actions', methods=['POST'])
def groups(id):
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
    if 'type' not in action:
        return Response(json.dumps({"message": "type must be supplied"}), status=412, mimetype='application/json')
    typeUpper = action['type'].upper()
    if typeUpper == 'HOME':
        roku.home()
    elif typeUpper == 'BACK':
        roku.back()
    elif typeUpper == 'UP':
        spaces = int(action['command'])
        runRokuCommandXTimes(roku, spaces, 'up')
    elif typeUpper == 'DOWN':
        spaces = int(action['command'])
        runRokuCommandXTimes(roku, spaces, 'down')
    elif typeUpper == 'LEFT':
        spaces = int(action['command'])
        runRokuCommandXTimes(roku, spaces, 'left')
    elif typeUpper == 'RIGHT':
        spaces = int(action['command'])
        runRokuCommandXTimes(roku, spaces, 'right')
    elif typeUpper == 'ENTER':
        roku.enter()
    elif typeUpper == 'SELECT':
        roku.select()
    elif typeUpper == 'PLAY':
        roku.play()
    elif typeUpper == 'PAUSE':
        roku.play()
    elif typeUpper == 'FORWARD':
        roku.forward()
    elif typeUpper == 'REVERSE':
        roku.reverse()
    elif typeUpper == 'SEARCH':
        searchTerm = action['command'].lower()
        roku.search()
        roku.literal(searchTerm)
    elif typeUpper == 'INPUT':
        app = roku[action['command']]
        app.launch()
    else:
        return Response(json.dumps({"message": "Action type " + typeUpper + " could not be found."}), status=412, mimetype='application/json')

    return Response(json.dumps({"message": "success"}), status=201, mimetype='application/json')


def runRokuCommandXTimes(roku, x, command):
    for i in range(x):
        getattr(roku, command)()
        sleep(1)
