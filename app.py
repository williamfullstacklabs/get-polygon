from flask import Flask
from flask_restful import Api

from resources.polygon import Polygon

app = Flask(__name__)
api = Api(app)

api.add_resource(Polygon, "/get")

if __name__ == "__main__":
  app.run()