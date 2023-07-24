from app import db

class MeetingType(db.Model):
    __tablename__ = 'meetingtype'

    id = db.Column('MeetingTypeID', db.Integer, primary_key=True, autoincrement=True)
    type = db.Column('Type', db.String(256))

    def __init__(self, type):
      self.type = type
      
    @classmethod
    def get_by_id(cls, id):
     return cls.query.filter_by(id=id).first()
    
    
    def to_dict(self):
     return {
         'id': self.id,
         'type': self.type
     }
    
    def update(self, data):
     self.type = data.get('type', self.type)

