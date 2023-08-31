from app import db


class Zone(db.Model):
    __tablename__ = 'zone'

    id = db.Column('ZoneID', db.Integer, primary_key=True, autoincrement=True)
    zone_name = db.Column('ZoneName', db.String(256))
    timezone = db.Column('Timezone', db.String(64))


    def __init__(self, zone_name, timezone):
        self.zone_name = zone_name
        self.timezone = timezone

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
            'zone_name': self.zone_name,
            'timezone': self.timezone,
        }

    def update(self, data):
        self.zone_name = data.get('zone_name', self.zone_name)
        self.timezone = data.get('timezone', self.timezone)
