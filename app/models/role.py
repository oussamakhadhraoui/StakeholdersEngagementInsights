from app import db

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column('RoleID', db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column('RoleName', db.String(256))


    

    def __init__(self, role_name):
        self.role_name = role_name
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name
            }
    
    def update(self, data):
        self.role_name = data.get('role_name', self.role_name)

