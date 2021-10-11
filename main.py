from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

# Flask & SQL
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.sqlite3'
db = SQLAlchemy(app)
Bootstrap(app)

# TMD API
api_key = 'df28c967c1e49add898fa87171044017'
search_string = "Rambo"
params = {
    "api_key": api_key,
    "language": "en-US",
    "query": search_string,
    "page": 1
}

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    year = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(250))


if not os.path.isfile("sqlite:///movies.sqlite3"):
    db.create_all()

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)


@app.route("/")
def home():
    all_movies = [movie for movie in db.session.query(Movie).all()]
    return render_template("index.html", movies=all_movies)


@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        edit_movie = Movie.query.get(id)
        new_rating = request.form["new_rating"]
        edit_movie.rating = new_rating
        db.session.commit()
        all_movies = [movie for movie in db.session.query(Movie).all()]
        return render_template("index.html", movies=all_movies)
    else:
        edit_movie = Movie.query.get(id)
        return render_template("edit.html", movie=edit_movie)


@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    edit_movie = Movie.query.get(id)
    db.session.delete(edit_movie)
    db.session.commit()
    all_movies = [movie for movie in db.session.query(Movie).all()]
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        all_movies = [movie for movie in db.session.query(Movie).all()]
        return render_template("index.html", movies=all_movies)
    else:
        response = requests.get(url="https://api.themoviedb.org/3/search/movie?", params=params).json()
        movie_request = response["results"]
        return render_template("add.html", movie=movie_request)


@app.route("/select")
def select():
#    title = movie_data["title"]
#    year = movie_data["release_date"]
#    description = movie_data["overview"]
#    rating = movie_data["vote_average"]
#    poster = movie_data["poster_path"]
#    img_url = f"https://image.tmdb.org/t/p/w500{poster}"
#    new_movie = Movie(title=title,
#                      year=year,
#                      description=description,
#                      rating=rating,
#                      img_url=img_url)
#    db.session.add(new_movie)
#    db.session.commit()


#if __name__ == '__main__':
#    app.run(debug=True)
