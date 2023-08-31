from app import db

class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column('CountryID', db.Integer, primary_key=True, autoincrement=True)
    zone_id = db.Column('ZoneID', db.Integer, db.ForeignKey('zone.ZoneID'))
    country_name = db.Column('CountryName', db.String(256))
    alpha2_code = db.Column('Alpha2Code', db.String(2))
    alpha3_code = db.Column('Alpha3Code', db.String(3))
    phone_prefix = db.Column('PhonePrefix', db.Integer)

    zone = db.relationship('Zone', backref='countries')

    def __init__(self, zone_id, country_name, alpha2_code, alpha3_code, phone_prefix):
        self.zone_id = zone_id
        self.country_name = country_name
        self.alpha2_code = alpha2_code
        self.alpha3_code = alpha3_code
        self.phone_prefix = phone_prefix

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
            'zone_id': self.zone_id,
            'country_name': self.country_name,
            'alpha2_code': self.alpha2_code,
            'alpha3_code': self.alpha3_code,
            'phone_prefix': self.phone_prefix
        }

    def update(self, data):
        self.zone_id = data.get('zone_id', self.zone_id)
        self.country_name = data.get('country_name', self.country_name)
        self.alpha2_code = data.get('alpha2_code', self.alpha2_code)
        self.alpha3_code = data.get('alpha3_code', self.alpha3_code)
        self.phone_prefix = data.get('phone_prefix', self.phone_prefix)
