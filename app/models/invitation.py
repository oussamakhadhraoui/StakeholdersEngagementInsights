from app import db

class Invitation(db.Model):
    __tablename__ = 'invitation'

    id = db.Column('InvitationID', db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column('MeetingID', db.Integer, db.ForeignKey('meeting.MeetingID'))
    person_id = db.Column('PersonID', db.Integer, db.ForeignKey('person.PersonID'))
    role_id = db.Column('RoleID', db.Integer, db.ForeignKey('role.RoleID'))
    status = db.Column('Status', db.Enum('Required', 'Optional'))


    meeting = db.relationship('Meeting', backref=db.backref('invitations', lazy=True))
    person = db.relationship('Person', backref=db.backref('invitations', lazy=True))
    role = db.relationship('Role', backref=db.backref('invitations', lazy=True))

    

    

    def __init__(self, meeting_id, person_id, role_id, status):
        self.meeting_id = meeting_id
        self.person_id = person_id
        self.role_id = role_id
        self.status = status
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def to_dict(self):
     return {
        'id': self.id,
        'meeting_id': self.meeting_id,
        'title': self.meeting.title if self.meeting else None,
        'person_id': self.person_id,
        'email': self.person.email if self.person else None,
        'role_id': self.role_id,
        'role_name': self.role.role_name if self.role else None,
        'status': self.status if self.status else None
    }

    
    def update(self, data):
        self.meeting_id = data.get('meeting_id', self.meeting_id)
        self.person_id = data.get('person_id', self.person_id)
        self.role_id = data.get('role_id', self.role_id)
        self.status = data.get('status', self.status)


