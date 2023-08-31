from app import db
from datetime import date

class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column('RoleID', db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column('RoleName', db.String(256))
    status = db.Column('Status', db.String(256), nullable=True)  
    join_date = db.Column('JoinDate', db.Date, nullable=True)  
    leave_date = db.Column('LeaveDate', db.Date, nullable=True) 

    def __init__(self, role_name, status=None, join_date=None, leave_date=None):
        self.role_name = role_name
        self.status = status
        self.join_date = join_date
        self.leave_date = leave_date
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def to_dict(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'status': self.status,
            'join_date': self.join_date.isoformat() if self.join_date else None,
            'leave_date': self.leave_date.isoformat() if self.leave_date else None
        }
    
    def update(self, data):
        self.role_name = data.get('role_name', self.role_name)
        self.status = data.get('status', self.status)
        self.join_date = data.get('join_date', self.join_date)
        self.leave_date = data.get('leave_date', self.leave_date)
