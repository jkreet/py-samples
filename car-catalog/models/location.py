from app import db
# from models.car import Car

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    cars = db.relationship('Car')

    # cars = db.relationship('Car', primaryjoin="or_(Car.base_location_id==Location.id, Car.current_location_id==Location.id)")

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'cars': self.cars
        }

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<id: {}, name: {}>'.format(self.id, self.name)