from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
    # Clean up any legacy movies that might be missing images or have placeholder data
    # This ensures your new cinematic grid stays professional.
    all_movies = Movie.query.all()
    for movie in all_movies:
        if not movie.img_url or "placeholder" in movie.img_url or len(movie.img_url) < 10:
            db.session.delete(movie)
    db.session.commit()

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

third_movie = Movie(
    title="Interstellar",
    year=2014,
    description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    rating=8.7,
    ranking=8,
    review="A visual and emotional masterpiece about time and love.",
    img_url="https://image.tmdb.org/t/p/w500/yQvGrMoipbRoddT0ZR8tPoR7NfX.jpg"
)

fourth_movie = Movie(
    title="The Matrix",
    year=1999,
    description="A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    rating=8.7,
    ranking=7,
    review="Changed sci-fi cinema forever. Red pill all the way.",
    img_url="https://image.tmdb.org/t/p/w500/aOIuZAjPaRIE6CMzbazvcHuHXDc.jpg"
)

fifth_movie = Movie(
    title="Pulp Fiction",
    year=1994,
    description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    rating=8.9,
    ranking=6,
    review="Tarantino at his absolute peak. The dialogue is gold.",
    img_url="https://image.tmdb.org/t/p/w500/vQWk5YBFWF4bZaofAbv0tShwBvQ.jpg"
)

sixth_movie = Movie(
    title="The Shawshank Redemption",
    year=1994,
    description="Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.",
    rating=9.3,
    ranking=5,
    review="The ultimate story of hope and friendship.",
    img_url="https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg"
)

seventh_movie = Movie(
    title="Spider-Man: Across the Spider-Verse",
    year=2023,
    description="Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence.",
    rating=8.9,
    ranking=4,
    review="The animation style is mind-blowing. A modern classic.",
    img_url="https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg"
)

eighth_movie = Movie(
    title="Gladiator",
    year=2000,
    description="A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
    rating=8.5,
    ranking=3,
    review="Are you not entertained?! Epic in every sense.",
    img_url="https://image.tmdb.org/t/p/w500/wN2xWp1eIwCKOD0BHTcErTBv1Uq.jpg"
)

ninth_movie = Movie(
    title="The Godfather",
    year=1972,
    description="Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone surviving an attempt on his life, his youngest son, Michael, steps in to take care of the killers.",
    rating=9.2,
    ranking=2,
    review="An offer you can't refuse. Best movie ever made?",
    img_url="https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
)

tenth_movie = Movie(
    title="Fight Club",
    year=1999,
    description="A ticking-time bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy.",
    rating=8.4,
    ranking=1,
    review="The first rule of Fight Club is: you do not talk about Fight Club.",
    img_url="https://image.tmdb.org/t/p/w500/hZkgoQYus5vegHoetLkCJzb17zJ.jpg"
)

eleventh_movie = Movie(
    title="Avengers: Endgame",
    year=2019,
    description="After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions.",
    rating=8.3,
    ranking=0,
    review="A perfect conclusion to a decade of storytelling.",
    img_url="https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
)

with app.app_context():
    if not Movie.query.filter_by(title="Inception").first():
        db.session.add(new_movie)
    if not Movie.query.filter_by(title="The Dark Knight").first():
        db.session.add(second_movie)
    if not Movie.query.filter_by(title="Interstellar").first():
        db.session.add(third_movie)
    if not Movie.query.filter_by(title="The Matrix").first():
        db.session.add(fourth_movie)
    if not Movie.query.filter_by(title="Pulp Fiction").first():
        db.session.add(fifth_movie)
    if not Movie.query.filter_by(title="The Shawshank Redemption").first():
        db.session.add(sixth_movie)
    if not Movie.query.filter_by(title="Spider-Man: Across the Spider-Verse").first():
        db.session.add(seventh_movie)
    if not Movie.query.filter_by(title="Gladiator").first():
        db.session.add(eighth_movie)
    if not Movie.query.filter_by(title="The Godfather").first():
        db.session.add(ninth_movie)
    if not Movie.query.filter_by(title="Fight Club").first():
        db.session.add(tenth_movie)
    if not Movie.query.filter_by(title="Avengers: Endgame").first():
        db.session.add(eleventh_movie)
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
