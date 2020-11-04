from flask_restful import Resource

import numpy as np
from flask import request
from requests.utils import quote
from skimage.measure import find_contours, points_in_poly, approximate_polygon
from skimage import io
from skimage import color
from threading import Thread

class Polygon(Resource):
  def get(self):
    center_latitude = request.args.get('lat') ##put latitude here 
    center_longitude = request.args.get('lng') ##put longitude here 
    mapZoom = request.args.get('zoom')
    width = request.args.get('width')
    height = request.args.get('height')

    midX = int(width) / 2
    midY = int(height) / 2
    str_Center = center_latitude + "," + center_longitude
    str_Size = width + "x" + height
    # Styled google maps url showing only the buildings
    safeURL_Style = quote('feature:landscape.man_made|element:geometry.stroke|visibility:on|color:0xffffff|weight:1')
    urlBuildings = "http://maps.googleapis.com/maps/api/staticmap?center=" + str_Center + "&zoom=" + mapZoom + "&format=png32&sensor=false&size=" + str_Size + "&maptype=roadmap&style=visibility:off&style=" + safeURL_Style + "&key=AIzaSyAFLAidtaOcjxTdYaWan2NQ4y8f8tWe2N4"

    mainBuilding = None
    imgBuildings = io.imread(urlBuildings)
    gray_imgBuildings = color.rgb2gray(imgBuildings)
    # will create inverted binary image
    binary_imageBuildings = np.where(gray_imgBuildings > np.mean(gray_imgBuildings), 0.0, 1.0)
    contoursBuildings = find_contours(binary_imageBuildings, 0.1)

    for n, contourBuilding in enumerate(contoursBuildings):
      if (contourBuilding[0, 1] == contourBuilding[-1, 1]) and (contourBuilding[0, 0] == contourBuilding[-1, 0]):
        # check if it is inside any other polygon, so this will remove any additional elements
        isInside = False
        skipPoly = False
        for othersPolygon in contoursBuildings:
          isInside = points_in_poly(contourBuilding, othersPolygon)
          if all(isInside):
            skipPoly = True
            break

          if skipPoly == False:
            center_inside = points_in_poly(np.array([[midX, midY]]), contourBuilding)
            if center_inside:
              # approximate will generalize the polygon
              mainBuilding = approximate_polygon(contourBuilding, tolerance=2)

    a = np.array(mainBuilding).tolist()
    return a, 200