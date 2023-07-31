from app import db


class Meeting(db.Model):
    __tablename__ = 'meeting'

    id = db.Column('MeetingID', db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column('MeetingTypeID', db.Integer, db.ForeignKey('meetingtype.MeetingTypeID'))
    start_date = db.Column('StartDate', db.Date)
    start_time = db.Column('StartTime', db.Time)
    end_date = db.Column('EndDate', db.Date)
    end_time = db.Column('EndTime', db.Time)
    location = db.Column('Location', db.String(256))
    title = db.Column('Title', db.String(256))  

    meetingtype = db.relationship('MeetingType', backref='meetings')
    

    def __init__(self, type_id, start_date, start_time, end_date, end_time, location, title):  
        self.type_id = type_id
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.location = location
        self.title = title  

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def delete(cls, id):
     obj = cls.get_by_id(id)
     if obj:
        db.session.delete(obj)
        db.session.commit()
        return True
     return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'type_id': self.type_id,
            'type': self.meetingtype.type if self.meetingtype else None,
            'start_date': self.start_date.isoformat(),
            'start_time': self.start_time.strftime('%I:%M %p') if self.start_time else None,
            'end_date': self.end_date.isoformat(),
            'end_time': self.end_time.strftime('%I:%M %p') if self.end_time else None,
            'location': self.location,
            'title': self.title  
        }

    def update(self, data):
        self.type_id = data.get('type_id', self.type_id)
        self.start_date = data.get('start_date', self.start_date)
        self.start_time = data.get('start_time', self.start_time)
        self.end_date = data.get('end_date', self.end_date)
        self.end_time = data.get('end_time', self.end_time)
        self.location = data.get('location', self.location)
        self.title = data.get('title', self.title)  
