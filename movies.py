import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'hard to guess secure key'

# setup SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    movies = db.relationship('Movie', backref='actor', cascade="delete")

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    genre = db.Column(db.String(256))
    year = db.Column(db.Integer)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))



@app.route('/')
def index():
    # return HTML
    # return "<h1>this is the index page!<h1>"
    return render_template('index.html')


@app.route('/members')
def about():
    return render_template('members.html')

@app.route('/actors')
def show_all_actors():
    actors = Actor.query.all()
    return render_template('actor-all.html', actors=actors)


@app.route('/actor/add', methods=['GET', 'POST'])
def add_actors():
    if request.method == 'GET':
        return render_template('actor-add.html')
    if request.method == 'POST':
        # get data from the form
        name = request.form['name']
        age = request.form['age']

        # insert the data into the database
        actor = Actor(name=name, age=age)
        db.session.add(actor)
        db.session.commit()
        return redirect(url_for('show_all_actors'))


@app.route('/actor/edit/<int:id>', methods=['GET', 'POST'])
def edit_actor(id):
    actor = Actor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('actor-edit.html', actor=actor)
    if request.method == 'POST':
        # update data based on the form data
        actor.name = request.form['name']
        actor.age = request.form['age']
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_actors'))

@app.route('/actor/delete/<int:id>', methods=['GET', 'POST'])
def delete_actor(id):
    actor = Actor.query.filter_by(id=id).first()
    if request.method == 'GET':
        return render_template('actor-delete.html', actor=actor)
    if request.method == 'POST':
        # delete the professor by id
        # all related courses are deleted as well
        db.session.delete(actor)
        db.session.commit()
        return redirect(url_for('show_all_actors'))



@app.route('/movies')
def show_all_movies():
    movies = Movie.query.all()
    return render_template('movie-all.html', movies=movies)

@app.route('/movie/add', methods=['GET', 'POST'])
def add_movies():
    if request.method == 'GET':
        actors = Actor.query.all()
        return render_template('movie-add.html', actors=actors)
    if request.method == 'POST':
        # get data from the form
        title = request.form['title']
        genre = request.form['genre']
        year = request.form['year']
        actor_name = request.form['actor']
        actor = Actor.query.filter_by(name=actor_name).first()
        movie = Movie(title=title, genre=genre, year=year, actor=actor)

        # insert the data into the database
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('show_all_movies'))


@app.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    actors = Actor.query.all()
    if request.method == 'GET':
        return render_template('movie-edit.html', movie=movie, actors=actors)
    if request.method == 'POST':
        # update data based on the form data
        movie.title = request.form['title']
        movie.genre = request.form['genre']
        movie.year = request.form['year']
        actor_name = request.form['actor']
        actor = Actor.query.filter_by(name=actor_name).first()
        movie.actor = actor
        # update the database
        db.session.commit()
        return redirect(url_for('show_all_movies'))

@app.route('/movie/delete/<int:id>', methods=['GET', 'POST'])
def delete_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    actors = Actor.query.all()
    if request.method == 'GET':
        return render_template('movie-delete.html', movie=movie, actors=actors)
    if request.method == 'POST':
        # use the id to delete the song
        # song.query.filter_by(id=id).delete()
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('show_all_movies'))






# https://goo.gl/Pc39w8 explains the following line
if __name__ == '__main__':

    # activates the debugger and the reloader during development
    # app.run(debug=True)
    app.run()

    # make the server publicly available on port 80
    # note that Ports below 1024 can be opened only by root
    # you need to use sudo for the following conmmand
    # app.run(host='0.0.0.0', port=80)
