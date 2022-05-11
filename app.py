from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    release_year = db.Column(db.Integer)
    genre = db.Column(db.String, nullable=False)
    mpaa_rating = db.Column(db.String)
    poster_image = db.Column(db.String, unique=True)

    def __init__(self, title, release_year, genre, mpaa_rating, poster_image):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.mpaa_rating = mpaa_rating
        self.poster_image = poster_image

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id','title','release_year','genre','mpaa_rating','poster_image')

movie_schema = MovieSchema()
multi_movie_schema = MovieSchema(many=True)

@app.route('/movie/add', methods=["POST"])
def add_movie():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON!')

    post_data = request.get_json()
    title = post_data.get('title')
    release_year = post_data.get('release_year')
    genre = post_data.get('genre')
    mpaa_rating = post_data.get('mpaa_rating')
    poster_image = post_data.get('poster_image')

    if title == None:
        return jsonify('Error: You must provide a Title!')
    if genre == None:
        return jsonify('Error: You must provide a Genre!')

    new_record = Movie(title, release_year, genre, mpaa_rating, poster_image)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(movie_schema.dump(new_record))
#  Get All Movies
@app.route('/movie/get', methods=["GET"])
def get_all_movies():
    all_records = db.session.query(Movie).all()
    return jsonify(multi_movie_schema.dump(all_records))

#  Get One Movie By Id
@app.route('/movie/get/<id>', methods=["GET"])
def get_movie_id(id):
    one_movie = db.session.query(Movie).filter(Movie.id == id).first()
    return jsonify(movie_schema.dump(one_movie))

#  Delete Movie
@app.route('/movie/delete/<id>', methods=["DELETE"])
def movie_to_delete(id):
    delete_movie = db.session.query(Movie).filter(Movie.id == id).first()
    db.session.delete(delete_movie)
    db.session.commit()
    return jsonify("The Movie You Selected for Deletion is Gone!")

# Update/Edit Movie
@app.route('/movie/update/<id>', methods=["PUT"])
def update_movie_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON!')

    put_data = request.get_json()
    title = put_data.get('title')
    release_year = put_data.get('release_year')
    genre = put_data.get('genre')
    mpaa_rating = put_data.get('mpaa_rating')
    poster_image = put_data.get('poster_image')

    movie_to_update = db.session.query(Movie).filter(Movie.id == id).first()

    if title != None:
        movie_to_update.title = title
    if release_year != None:
        movie_to_update.release_year = release_year
    if genre != None:
        movie_to_update.genre = genre
    if mpaa_rating != None:
        movie_to_update.mpaa_rating = mpaa_rating
    if poster_image != None:
        movie_to_update.poster_image = poster_image

    db.session.commit()
    return jsonify(movie_schema.dump(movie_to_update))
    




    







if __name__ == "__main__":
    app.run(debug = True)