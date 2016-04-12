from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


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
