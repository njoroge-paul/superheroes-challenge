#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Heroes(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict() for hero in heroes]

class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero is None:
            return {"error": f"Hero with ID {id} not found"}, 404
        return hero.to_dict()

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict() for power in powers]

class PowerResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power is None:
            return {"error": "Power not found"}, 404
        return power.to_dict()

    def patch(self, id):
        power = Power.query.get(id)
        if power is None:
            return {"error": "Power not found"}, 404
        data = request.get_json()
        power.description = data.get("description")
        try:
            db.session.commit()
            return power.to_dict()
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        hero_id = data.get("hero_id")
        power_id = data.get("power_id")
        strength = data.get("strength")
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        if hero is None or power is None:
            return {"error": "Hero or Power not found"}, 404
        hero_power = HeroPower(hero=hero, power=power, strength=strength)
        try:
            db.session.add(hero_power)
            db.session.commit()
            return hero_power.to_dict()
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowerResource, '/powers/<int:id>')
api.add_resource(HeroPowers, '/hero_powers')

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)