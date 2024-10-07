from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    powers = relationship('HeroPower', backref='hero', lazy=True)

    serialize_rules = ('-powers.power',)

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    heroes = relationship('HeroPower', backref='power', lazy=True)

    serialize_rules = ('-heroes.hero',)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('Name cannot be empty')
        return name

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise AssertionError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    serialize_rules = ('-hero', '-power')

    @validates('strength')
    def validate_strength(self, key, strength):
        if not strength or strength not in ['Strong', 'Weak', 'Average']:
            raise AssertionError('Strength must be one of Strong, Weak, or Average')
        return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'