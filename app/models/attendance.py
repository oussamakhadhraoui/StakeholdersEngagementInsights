from app import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column('AttendanceID', db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column('PersonID', db.Integer, db.ForeignKey('person.PersonID'))
    meeting_id = db.Column('MeetingID', db.Integer, db.ForeignKey('meeting.MeetingID'))
    attendance_duration = db.Column('AttendanceDuration', db.Time)

    person = db.relationship('Person', backref='attendances')
    meeting = db.relationship('Meeting', backref='attendances')

    def __init__(self, person_id, meeting_id, attendance_duration):
        self.person_id = person_id
        self.meeting_id = meeting_id
        self.attendance_duration = attendance_duration

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
        'person_id': self.person_id,
        'person_email': self.person.email if self.person else None,
        'meeting_id': self.meeting_id,
        'meeting_title': self.meeting.title if self.meeting else None,
        'start_date' : self.meeting.start_date if self.meeting else None,
        'attendance_duration': self.attendance_duration.strftime('%H:%M:%S') if self.attendance_duration else None
    }


    def update(self, data):
        self.person_id = data.get('person_id', self.person_id)
        self.meeting_id = data.get('meeting_id', self.meeting_id)
        self.attendance_duration = data.get('attendance_duration', self.attendance_duration)
