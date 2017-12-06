from flask_script import Manager
from movies import app, db, Actor, Movie

manager = Manager(app)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    damon = Actor(name='Matt Damon', age=45)
    db.session.add(damon)

db.session.commit()


if __name__ == "__main__":
    manager.run()
