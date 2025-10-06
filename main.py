from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)
Bootstrap5(app)
MOVIE_DB_SEARCH_KEY = os.getenv("MOVIE_DB_SEARCH_KEY_PASS")
MOVIE_DB_SEARCH_URL = os.getenv("MOVIE_DB_SEARCH_URL_PASS")
MOVIE_DB_INFO_URL = os.getenv("MOVIE_DB_INFO_URL_PASS")
MOVIE_DB_IMAGE_URL = os.getenv("MOVIE_DB_IMAGE_URL_PASS")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_PASS")
# CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_PASS")
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), unique=False,nullable=False)
    year : Mapped[int] = mapped_column(Integer, nullable=False)
    description : Mapped[str] = mapped_column(String(250), nullable=False)
    rating : Mapped[float] = mapped_column(Float, nullable=True)
    ranking : Mapped[int] = mapped_column(Integer, nullable=True)
    review : Mapped[str] = mapped_column(String(250), nullable=True)
    img_url : Mapped[str] = mapped_column(String(250), nullable=False)
with app.app_context():
    db.create_all()

class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title")
    submit = SubmitField("Add Movie")



new_movie = Movie(
    title="Inception",
    year=2010,
    description="A skilled thief is given a chance at redemption if he can successfully perform an inception: planting an idea into someone's subconscious.",
    rating=8.8,
    ranking=10,
    review="Mind-bending story with stunning visuals!",
    img_url="https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"
)
second_movie = Movie(
    title="The Dark Knight",
    year=2008,
    description="Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos and challenges the very essence of justice.",
    rating=9.0,
    ranking=9,
    review="Heath Ledger's Joker is legendary.",
    img_url="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
)

with app.app_context():
    if not Movie.query.filter_by(title="Inception").first():
        db.session.add(new_movie)
    if not Movie.query.filter_by(title="The Dark Knight").first():
        db.session.add(second_movie)
    db.session.commit()

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_SEARCH_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)


    return render_template("add.html", form=form)



@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie,movie_id)
    if form.validate_on_submit():
        try:
            movie.rating = float(form.rating.data)
        except ValueError:
            movie.rating = movie.rating
        finally:
            movie.review = form.review.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',movie=movie,form=form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_SEARCH_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()

        # Redirect to /edit route
        return redirect(url_for("edit", id=new_movie.id))




@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie,movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))




if __name__ == '__main__':
    app.run(debug=True)
