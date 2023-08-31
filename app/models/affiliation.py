from app import db

class Affiliation(db.Model):
    __tablename__ = 'affiliation'

    affiliation_id = db.Column('AffiliationID', db.String(256), primary_key=True)
    affiliation_name = db.Column('AffiliationName', db.String(256), nullable=False)
    parent_affiliation_id = db.Column('ParentAffiliationID', db.String(256), db.ForeignKey('affiliation.AffiliationID', ondelete='SET NULL'))
    parent_affiliation_name = db.Column('ParentAffiliationName', db.String(256))
    label = db.Column('Label', db.String(256), nullable=True)

    parent_aff = db.relationship('Affiliation', remote_side=[affiliation_id], backref='child_affiliations')

    def __init__(self, affiliation_id, affiliation_name, label=None, parent_affiliation_id=None, parent_affiliation_name=None):
        self.affiliation_id = affiliation_id
        self.affiliation_name = affiliation_name
        self.label = label
        self.parent_affiliation_id = parent_affiliation_id if parent_affiliation_id is not None else None
        self.parent_affiliation_name = parent_affiliation_name

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(affiliation_name=name).first()

    @classmethod
    def get_by_id(cls, affiliation_id):
        return cls.query.filter_by(affiliation_id=affiliation_id).first()

    def to_dict(self):
        return {
            'affiliation_id': self.affiliation_id,
            'affiliation_name': self.affiliation_name,
            'parent_affiliation_id': self.parent_affiliation_id,
            'parent_affiliation_name': self.parent_affiliation_name,
            'label': self.label,
        }

    def update(self, data):
        self.affiliation_id = data.get('affiliation_id', self.affiliation_id)
        self.affiliation_name = data.get('affiliation_name', self.affiliation_name)
        self.label = data.get('label', self.label)
        if 'parent_affiliation_id' in data:
            self.parent_affiliation_id = data['parent_affiliation_id'] if data['parent_affiliation_id'] is not None else None
        if 'parent_affiliation_name' in data:
            self.parent_affiliation_name = data['parent_affiliation_name']
