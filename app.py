import json
import os
from sqlalchemy.sql.functions import count
from django.contrib.admin.templatetags.admin_list import results

from flask import Flask, jsonify, abort, request, Response, g, flash
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from models import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)




@app.route('/')
def home():
    return render_template('index.html')


@app.route('/parks', methods=['GET'])
def parks():
    parkss = Park.query.all()

    list = [park.as_dict() for park in parkss]
    js = json.dumps(list)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'

    # result = [park.as_dict() for park in parks]
    return resp


@app.route('/parks/<int:parkid>', methods=['GET', 'POST', 'DELETE'])
def park_id(parkid):
    if request.method == 'GET':
        us = db.session.query(Park).filter_by(idpark=parkid).first()

        if us == None:
            return not_found()
        else:
            resp = Response(json.dumps(us.as_dict()), status=200, mimetype='application/json')
            resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'
            return resp
    if request.method == 'POST':
        return 'POST'
    if request.method == 'DELETE':
        return 'DELETE'
    else:
        return not_found()


@app.route('/parks/add', methods=['POST'])
def add_park():
    if request.method == 'POST':
        name = request.args.get('name')
        city = request.args.get('city')
        street = request.args.get('street')
        street_nr = request.args.get('street_nr')

        try:

            db.create_all()
            db.session.add(Park(name, street, street_nr, city))
            #g.db.commit()
            db.session.commit()
        except Exception as e:
            return e.message

        return 'Everythings is ok!'
    else:

        return 'Something is wrong'


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
