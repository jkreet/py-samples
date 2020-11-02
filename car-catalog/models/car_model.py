from app import db
# from models.car import Car

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    year = db.Column(db.String(4))

    car = db.relationship('Car')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year
        }

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Name: {}, Year: {}>'.format(self.name, self.year)
