import json
import os
from sqlalchemy.sql.functions import count
from django.contrib.admin.templatetags.admin_list import results

from flask import Flask, jsonify, abort, request, Response, g, flash
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loginu = db.Column(db.String)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, surname, loginu, email):
        self.name = name
        self.email = email
        self.surname = surname
        self.loginu = loginu

    def __repr__(self):
        return '<Name %r %r> Email %r' % self.name, self.surname, self.email


class Cars(db.Model):
    idcar = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nrrej = db.Column(db.String(9))
    iduser = db.Column(db.Integer)  # dopisac foreign key User id
    mark = db.Column(db.String(20))


class Park(db.Model):
    idpark = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    street = db.Column(db.String(30))
    street_nr = db.Column(db.Integer)
    city = db.Column(db.String(20))

    def __init__(self, name, str, str_nr, ci):
        self.name = name
        self.street = str
        self.street_nr = str_nr
        self.city = ci

    def as_dict(self):
        obc_dict = {
            'ID': self.idpark,
            'Nazwa': self.name,
            'Ulica': self.street,
            'Nr_ulicy': self.street_nr,
            'Miasto': self.city
        }
        return obc_dict


# create table Stanowiska
# (IDStanowiska int primary key identity(1,1)
# ,Nazwa nvarchar(10)
# ,IDParkingu int foreign key references Parking(IDParkingu)
# ,NrStanowiska int
# ,PozycjaX int
# ,PozycjaY int
# ,unique(IDParkingu, NrStanowiska)
# )

# create table Przydzial
# (IDPrzydzialu int primary key identity(1,1)
# ,IDStanowiska int foreign key references Stanowiska(IDStanowiska)
# ,IDSamochodu int foreign key references Samochody(IDSamochodu)
# --,IDUzytkownika int foreign key references Uzytkownicy(IDUzytkownika)
# ,DataRezerwacji datetime default(getDate())
# ,RezerwacjaOd datetime
# ,RezerwacjaDo datetime
# ,KodDostepu nvarchar(20)
# ,KodQr image
# ,CzyZajete nvarchar(3) default 'Nie'
# )


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

        newpark = Park(name, street, street_nr, city)

        # #return 'ok'
        # #if newpark != None:
        # from app import Park

        #g.db.execute('insert into Park (na, str, strnr, ci) values (?, ?, ?, ?)', [name, street, street_nr, city])
        #g.db.commit()
        #flash('New entry was successfully posted')

        try:

            db.create_all()
            db.session.add(Park(name, street, street_nr, city))
            #g.db.commit()
            db.session.commit()
        except Exception as e:
            return e.message

        resp = Response(json.dumps(newpark.as_dict()), status=200, mimetype='application/json')
        resp.headers['Link'] = 'https://polar-plains-14145.herokuapp.com'

        return resp
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
