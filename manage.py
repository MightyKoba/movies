from flask_script import Manager
from movies import app, db, Actor, Movie

manager = Manager(app)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    damon = Actor(name='Matt Damon', age=45)
    titanic = Movie(title='Titanic', genre='Drama/Romance' , year=1999 , actor='Leonardo DiCaprio')
    db.session.add(damon)
    db.session.add(titanic)

    db.session.commit()


if __name__ == "__main__":
    manager.run()
