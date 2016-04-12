import os
from sqlalchemy.sql.functions import count
from django.contrib.admin.templatetags.admin_list import results

from flask import Flask, jsonify, abort, request
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
    iduser = db.Column(db.Integer)      # dopisac foreign key User id
    mark = db.Column(db.String(20))

class Park(db.Model):
    idpark = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    street = db.Column(db.String(30))
    street_nr = db.Column(db.Integer)
    city = db.Column(db.String(20))

    def as_dict(self):
        obc_dict = {
            'ID':self.idpark,
            'Nazwa':self.name,
            'Ulica':self.street,
            'Nr_ulicy':self.street_nr,
            'Miasto':self.city
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


@app.route('/parks')
def parks():

    parkss = Park.query.all()
    result = [park.as_dict() for park in parks]
    return jsonify({count: len(result), results: result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)