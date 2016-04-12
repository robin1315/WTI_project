from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

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
