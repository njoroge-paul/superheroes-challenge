from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Power.query.delete()
        Hero.query.delete()
        HeroPower.query.delete()

        print("Seeding powers...")
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]

        db.session.add_all(powers)

        print("Seeding heroes...")
        heroes = [
            Hero(id=1, name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(id=2, name="Doreen Green", super_name="Squirrel Girl"),
            Hero(id=3, name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(id=4, name="Janet Van Dyne", super_name="The Wasp"),
            Hero(id=5, name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(id=6, name="Carol Danvers", super_name="Captain Marvel"),
            Hero(id=7, name="Jean Grey", super_name="Dark Phoenix"),
            Hero(id=8, name="Ororo Munroe", super_name="Storm"),
            Hero(id=9, name="Kitty Pryde", super_name="Shadowcat"),
            Hero(id=10, name="Elektra Natchios", super_name="Elektra"),
        ]

        db.session.add_all(heroes)

        print("Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []
        for i, hero in enumerate(heroes):
            power = Power.query.all()[i % len(powers)]
            hero_powers.append(
                HeroPower(hero=hero, power=power, strength="Average")
            )
        db.session.add_all(hero_powers)
        db.session.commit()

        print("Done seeding!")