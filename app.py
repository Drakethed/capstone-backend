from pydoc import describe
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)

    def __init__(self, title, price, genre, description, img_url):
        self.title = title
        self.price = price
        self.genre = genre
        self.description = description
        self.img_url = img_url

class MovieSchema(ma.Schema):
        class Meta:
          fields = ("id", "title", "price", "genre", "description", "img_url")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/add-movie", methods=["POST"])
def add_movie():
    title = request.json.get("title")
    description = request.json.get("description")
    genre = request.json.get("genre")
    price = request.json.get("price")
    img_url = request.json.get("img_url")

    record = Movies(title, price, genre, description, img_url)
    db.session.add(record)
    db.session.commit()

    return jsonify(movie_schema.dump(record))



@app.route("/movies", methods=["GET"])
def get_all_movies():
    all_movies = Movies.query.all()
    return jsonify(movies_schema.dump(all_movies))



@app.route("/movie/<id>", methods=["DELETE","GET","PUT"])
def movie_id(id):
    movie = Movies.query.get(id)
    if request.method == "DELETE":
        db.session.delete(movie)
        db.session.commit()
    
        return movie_schema.jsonify(movie)
    elif request.method == "PUT":
        title = request.json['title']
        genre = request.json['genre']
        price = request.json['price']
        description = request.json['description']
        img_url = request.json['img_url']

        movie.title = title
        movie.genre = genre
        movie.price = price
        movie.description = description
        movie.img_url = img_url

        db.session.commit()
        return movie_schema.jsonify(movie)
    elif request.method == "GET":
        return movie_schema.jsonify(movie)



if __name__ == "__main__":
    app.run(debug=True)



