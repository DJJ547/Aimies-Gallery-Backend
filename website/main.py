from flask import Flask, \
    session, \
    Response, \
    jsonify, \
    make_response, \
    request, \
    json
# from flask_cors import CORS
import requests
# import packages
import datetime

import google.cloud.storage
from io import BytesIO
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import PIL.Image
from IPython.display import Image
import sys
import os

from arts.images import generate_image_names_and_links
from arts.images import generate_random_display_image_links

api_version = "/api"


app = Flask(__name__)
# CORS(app)


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route(api_version + "/arts/<art_type>")
def get_all_image_links(art_type):
    bucket_name = 'aimiefung-art.com'
    output = generate_image_names_and_links(bucket_name, art_type)
    return Response(json.dumps(output), status=200)


@app.route(api_version + "/home")
def get_random_display_image_links():
    bucket_name = 'aimiefung-art.com'
    output = generate_random_display_image_links(bucket_name)
    return Response(json.dumps(output), status=200)


if __name__ == '__main__':
    app.run(debug=True)
