from app import db

class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column('PersonID', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column('FirstName', db.String(256))
    last_name = db.Column('LastName', db.String(256))
    email = db.Column('Email', db.String(256))
    phone = db.Column('Phone', db.String(256))
    address = db.Column('Address', db.String(256))
    affiliation_id = db.Column('AffiliationID', db.String(256), db.ForeignKey('affiliation.AffiliationID'))
    manager_id = db.Column('ManagerID', db.Integer, db.ForeignKey('person.PersonID'))
    country_id = db.Column('CountryID', db.Integer, db.ForeignKey('country.CountryID'))

    affiliation = db.relationship('Affiliation', backref='people')
    country = db.relationship('Country', backref='residents')
    manager = db.relationship('Person', remote_side=[person_id], backref='subordinates')

    def __init__(self, first_name, last_name, email, phone, address, affiliation_id, country_id, manager_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.affiliation_id = affiliation_id
        self.country_id = country_id
        self.manager_id = manager_id if manager_id is not None else None

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(person_id=id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_name(cls, first_name, last_name):
       return cls.query.filter_by(first_name=first_name, last_name=last_name).first()


    def to_dict(self):
        return {
            'person_id': self.person_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'affiliation_id': self.affiliation_id,
            'affiliation_name': self.affiliation.affiliation_name if self.affiliation else None,
            'country_id': self.country_id,
            'country_alpha3_code': self.country.alpha3_code if self.country else None,
            'manager_id': self.manager_id
        }

    def update(self, data):
        self.first_name = data.get('first_name', self.first_name)
        self.last_name = data.get('last_name', self.last_name)
        self.email = data.get('email', self.email)
        self.phone = data.get('phone', self.phone)
        self.address = data.get('address', self.address)
        self.affiliation_id = data.get('affiliation_id', self.affiliation_id)
        self.country_id = data.get('country_id', self.country_id)
        if 'manager_id' in data:
            self.manager_id = data['manager_id'] if data['manager_id'] is not None else None
