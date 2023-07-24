from app import db

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column('PersonID', db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column('FirstName', db.String(256))
    last_name = db.Column('LastName', db.String(256))
    email = db.Column('Email', db.String(256))
    phone = db.Column('Phone', db.String(256))
    address = db.Column('Address', db.String(256))
    manager_id = db.Column('ManagerID', db.Integer, db.ForeignKey('person.PersonID', ondelete='SET NULL'))

    def __init__(self, first_name, last_name, email, phone, address, manager_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.manager_id = manager_id
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
        
    def to_dict(self):
     return {
         'id': self.id,
         'first_name': self.first_name,
         'last_name': self.last_name,
         'email': self.email,
         'phone': self.phone,
         'address': self.address,
         'manager_id': self.manager_id
     }
    
    def update(self, data):
     self.first_name = data.get('first_name', self.first_name)
     self.last_name = data.get('last_name', self.last_name)
     self.email = data.get('email', self.email)
     self.phone = data.get('phone', self.phone)
     self.address = data.get('address', self.address)
     self.manager_id = data.get('manager_id', self.manager_id)

