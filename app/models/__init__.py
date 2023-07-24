from app import db
from .meeting import Meeting
from .meetingtype import MeetingType
'''
from .personModel import Person
from .roleModel import Role
from .invitationModel import Invitation
'''

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Meeting(1, '2023-08-01', '09:00:00', '2023-08-01', '17:00:00', 'Secret Location'))
    db.session.commit()
    print('Database initialized!')
