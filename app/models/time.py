from app import db

class Time(db.Model):
    __tablename__ = 'time'

    date = db.Column('Date', db.Date, primary_key=True)
    year = db.Column('Year', db.Integer)
    month = db.Column('Month', db.Integer)
    day = db.Column('Day', db.Integer)
    week = db.Column('Week', db.Integer)
    weekday = db.Column('Weekday', db.String(10))
    quarter = db.Column('Quarter', db.Integer)

    def __init__(self, date, year, month, day, week, weekday, quarter):
        self.date = date
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.weekday = weekday
        self.quarter = quarter

    @classmethod
    def get_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    def to_dict(self):
        return {
            'date': self.date,
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'week': self.week,
            'weekday': self.weekday,
            'quarter': self.quarter
        }

    def update(self, data):
        self.year = data.get('year', self.year)
        self.month = data.get('month', self.month)
        self.day = data.get('day', self.day)
        self.week = data.get('week', self.week)
        self.weekday = data.get('weekday', self.weekday)
        self.quarter = data.get('quarter', self.quarter)
