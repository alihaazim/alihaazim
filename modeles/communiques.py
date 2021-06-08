from sqlalchemy import Column, Integer, String, PickleType, create_engine, MetaData
from marshmallow import Schema, fields, post_load
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root:1234@localhost/covid')
Session = sessionmaker(bind=engine)
session = Session()
meta = MetaData(engine)


class Communiques(Base):
    __tablename__ = 'communique'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(30))
    test_realise = Column(Integer, nullable=False)
    nouveaux_cas = Column(Integer, nullable=False)
    cas_contacts = Column(Integer, nullable=False)
    cas_communautaires = Column(Integer, nullable=False)
    cas_importes = Column(Integer, nullable=False)
    personne_sous_traitement = Column(Integer, nullable=False)
    nombre_gueris = Column(Integer, nullable=False)
    nombre_deces = Column(Integer, nullable=False)
    nom_fichier_source = Column(String(30), nullable=False)
    date_heure_extraction = Column(String(30), nullable=False)
    localites = Column(PickleType)

    def __init__(self, date, test_realise, nouveaux_cas, cas_contacts, cas_communautaires, cas_importes,
                 personne_sous_traitement, nombre_gueris, nombre_deces,
                 nom_fichier_source, date_heure_extraction, localites=dict):
        self.date = date
        self.test_realise = test_realise
        self.nouveaux_cas = nouveaux_cas
        self.cas_contacts = cas_contacts
        self.cas_communautaires = cas_communautaires
        self.cas_importes = cas_importes
        self.personne_sous_traitement = personne_sous_traitement
        self.nombre_gueris = nombre_gueris
        self.nombre_deces = nombre_deces
        self.nom_fichier_source = nom_fichier_source
        self.date_heure_extraction = date_heure_extraction
        self.localites = localites

    def init_DB(self):
        Base.metadata.create_all(bind=engine)
        session.add(self)
        session.commit()

        print("Initialized the db")


class CommuniqueSchema(Schema):
    date = fields.Str()
    test_realise = fields.Int()
    nouveaux_cas = fields.Int()
    cas_contacts = fields.Int()
    cas_communautaires = fields.Int()
    cas_importes = fields.Int()
    personne_sous_traitement = fields.Int()
    nombre_gueris = fields.Int()
    nombre_deces = fields.Int()
    nom_fichier_source = fields.Str()
    date_heure_extraction = fields.Str()
    localites = fields.Dict()

    @post_load()
    def make_user(self, data, **__):
        return Communiques(**data)


if __name__ == '__main__':
    schema = CommuniqueSchema()
