from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api

from resources.polygon import Polygon

app = Flask(__name__)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

api.add_resource(Polygon, "/get")

if __name__ == "__main__":
  app.run()