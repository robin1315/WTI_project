# _*_ coding: utf-8 _*_

import json
import os
import datetime

from flask import Flask, jsonify, request, Response
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def users():
    userss = User.query.all()

    list = [user.as_dict() for user in userss]
    js = json.dumps(list)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'
    return resp


@app.route('/users/<int:userid>', methods=['GET', 'POST', 'DELETE'])
def user_id(userid):
    if request.method == 'GET':
        us = db.session.query(User).filter_by(id=userid).first()

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


@app.route('/users/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        login = request.args.get('login')
        name = request.args.get('name')
        surname = request.args.get('surname')
        email = request.args.get('email')
        passw = request.args.get('password')


        try:
            db.session.add(User(login, name, surname, email, passw))
            db.session.commit()
        except Exception as e:
            return e.message

        return 'Everythings is ok!'
    else:

        return 'Something is wrong'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        loginn = request.args.get('login')
        passw = request.args.get('password')

        us = db.session.query(User).filter_by(loginu=loginn).first()

        if us == None:
            us = db.session.query(User).filter_by(email=loginn).first()
        if us == None:
            return "false"

        us_dict = us.as_dict()

        if us_dict.get('password') == passw:
            return Response(us_dict.get("ID"), status=200, mimetype='text/plain')
    if request.method == 'GET':
        return "false"

    else:
        return "false"


@app.route('/parks', methods=['GET'])
def parks():
    parkss = Park.query.all()
    list = [park.as_dict() for park in parkss]
    js = json.dumps(list)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'
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


@app.route('/parks_wsp', methods=['GET'])
def parks_wsp():
    parkss = Park.query.all()
    list = [park.as_dict_wsp() for park in parkss]
    js = json.dumps(list)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'
    return resp


@app.route('/parks_wsp/<int:parkid>', methods=['GET', 'POST', 'DELETE'])
def park_id_wsp(parkid):
    if request.method == 'GET':
        us = db.session.query(Park).filter_by(idpark=parkid).first()

        if us == None:
            return not_found()
        else:
            resp = Response(json.dumps(us.as_dict_wsp()), status=200, mimetype='application/json')
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
        wspX = request.args.get('wspX')
        wspY = request.args.get('wspY')

        try:
            db.session.add(Park(name, street, street_nr, city, wspX, wspY))
            db.session.commit()
        except Exception as e:
            return e.message

        return 'Everythings is ok!'
    else:

        return 'Something is wrong'


@app.route('/reservation/add', methods=['POST'])
def add_reservation():
    if request.method == 'POST':
        IdPlace = request.args.get('idplace')
        NrRegistration = request.args.get('nrregister')
        IdUser = request.args.get('iduser')
        #DateReservation = request.args.get('')
        ReservationFrom = request.args.get('from')
        ReservationTo = request.args.get('to')
        #todo generowanie kodu dostepu, kodu qr
        AccessCode = 'jakiskoddostepu'
        QRCode = 'qrkodjakis'
        #Busy = db.Column(db.Boolean, default=db.false)

        try:
            db.session.add(Allocation(IdPlace, NrRegistration, IdUser, ReservationFrom, ReservationTo, AccessCode, QRCode))
            db.session.commit()
        except Exception as e:
            return e.message

        return "Everythings is ok!"
    else:
        return 'NOT POST'

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp




####models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loginu = db.Column(db.String)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30), unique=True)

    def __init__(self, loginu, name, surname, email, password):
        self.name = name
        self.email = email
        self.surname = surname
        self.loginu = loginu
        self.password = password

    def __repr__(self):
        return '<Name %r %r> Email %r' % self.name, self.surname, self.email

    def as_dict(self):
        obc_dict = {
            'ID': self.id,
            'Login': self.loginu,
            'Imie': self.name,
            'Nazwisko': self.surname,
            'email': self.email,
            'password': self.password
        }
        return obc_dict

class Cars(db.Model):
    idcar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nrrej = db.Column(db.String(9))
    iduser = db.Column(db.Integer)  # dopisac foreign key User id
    mark = db.Column(db.String(20))


class Park(db.Model):
    #todo poprawic precyzjae wsp
    idpark = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    street = db.Column(db.String(30))
    street_nr = db.Column(db.Integer)
    city = db.Column(db.String(20))
    wspX = db.Column(db.FLOAT(precision=8))
    wspY = db.Column(db.FLOAT(precision=8))

    def __init__(self, name, stri, str_nr, ci, wspX, wspY):
        self.name = name
        self.street = stri
        self.street_nr = str_nr
        self.city = ci
        self.wspX = wspX
        self.wspY = wspY

    def as_dict(self):
        obc_dict = {
            'ID': self.idpark,
            'Nazwa': self.name,
            'Ulica': self.street,
            'Nr_ulicy': self.street_nr,
            'Miasto': self.city,
            'Wspolrzedna X': self.wspX,
            'Wspolrzedna Y': self.wspY
        }
        return obc_dict

    def as_dict_wsp(self):
        obc_dict = {
            'ID': self.idpark,
            'X': self.wspX,
            'Y': self.wspY
        }
        return obc_dict


class Allocation(db.Model):
    #todo pomyslec jak rozwiazac przechowywanie obrazow w bazie
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdPlace = db.Column(db.Integer, db.ForeignKey('place.Id'))
    NrRegistration = db.Column(db.String(9))
    IdUser = db.Column(db.Integer, db.ForeignKey('user.id'))
    DateReservation = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
    ReservationFrom = db.Column(db.DATETIME)
    ReservationTo = db.Column(db.DATETIME)
    AccessCode = db.Column(db.String)
    QRCode = db.Column(db.String)
    Busy = db.Column(db.Boolean, default=db.false)

    def __init__(self, idplace, nrreg, idus, resfrom, resto , access, qrcode ):
        self.IdPlace = idplace
        self.NrRegistration = nrreg
        self.IdUser = idus
        self.ReservationFrom = resfrom
        self.ReservationTo = resto
        self.AccessCode =access
        self.QRCode = qrcode

    def as_dict(self):
        obc_dict = {
            'ID': self.Id,
            'ID miejsca': self.IdPlace,
            'Numer rejestracji': self.NrRegistration,
            'ID Użytkownika': self.IdUser,
            'Data reserwacji': self.DateReservation,
            'Od': self.ReservationFrom,
            'Do': self.ReservationTo,
            'Kod dostepu': self.AccessCode,
            'QR kod': self.QRCode,
            'Zajete': self.Busy
        }
        return obc_dict


class Place(db.Model):

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IdPark = db.Column(db.Integer, db.ForeignKey('park.idpark'))
    NrPlace = db.Column(db.Integer)
    WspX = db.Column(db.FLOAT(precision=8) )
    WspY = db.Column(db.FLOAT(precision=8))

    def __init__(self, idpark, nrpl, wspx, wspy):
        self.IdPark = idpark
        self.NrPlace = nrpl
        self.WspX = wspx
        self.WspY = wspy

    def as_dict(self):
        obc_dict = {
            'ID': self.Id,
            'ID Parkingu': self.IdPark,
            'Numer miejsca': self.NrPlace,
            'WspX': self.WspX,
            'WspY': self.WspY
        }
        return obc_dict


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
