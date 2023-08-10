from flask import Flask, \
    session, \
    Response, \
    jsonify, \
    make_response, \
    request, \
    json
from flask_cors import CORS
import requests
import datetime

import google.cloud.storage
import sys
import logging
import os
import psycopg2

from website.arts.images import generate_image_names_and_links
from website.arts.images import generate_random_display_image_links

api_version = "/api"


app = Flask(__name__)
CORS(app)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/test")
def test():
    # Connect to the database
    conn = psycopg2.connect(database="d3705to6pu2soc",
                            user="fqgvalozkezayf",
                            password="14278285a3e302f98c45e79ccd5c2f91ad4596b8c16a3cb66c1e74e6771e4211",
                            host="ec2-3-233-174-23.compute-1.amazonaws.com", port="5432")

    # create a cursor
    cur = conn.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM students''')

    # Fetch the data
    data = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()

    return Response(json.dumps(data), status=200)


@app.route("/arts/<art_type>")
def get_all_image_links(art_type):
    bucket_name = 'aimiefung-art.com'
    output = generate_image_names_and_links(bucket_name, art_type)
    return Response(json.dumps(output), status=200)


@app.route("/home")
def get_random_display_image_links():
    bucket_name = 'aimiefung-art.com'
    output = generate_random_display_image_links(bucket_name)
    return Response(json.dumps(output), status=200)


if __name__ == '__main__':
    app.run(debug=True)
