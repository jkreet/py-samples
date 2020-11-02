from app import db
from models.car_model import Model
from models.location import Location

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    plate = db.Column(db.String(50), unique=True)
    avail = db.Column(db.Boolean, default=True)
    base_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    current_location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    year = db.Column(db.String(4))

    model = db.relationship(Model, back_populates='car')
    current_location = db.relationship(Location, back_populates='cars', foreign_keys=current_location_id)
    base_location = db.relationship(Location, foreign_keys=base_location_id)


    def __init__(self, *args, **kwargs):
        super(Car, self).__init__(*args, **kwargs)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'plate': self.plate,
            'avail': self.avail,
            'model' : self.model.serialize,
            'location': {
                'current': self.current_location.serialize,
                'base': self.base_location.serialize
            }
        }

