import datetime

from google.cloud import storage
from gcd.GoogleStorageClient import get_google_authentication
from gcdmysql.GcdMysqlConnector import GcdMysqlConnector
from gcdmysql.constant import PATH
from gcd.GoogleStorageClient import get_google_authentication


def generate_image_links(bucket_name, art_type):
    storage_client = get_google_authentication()
    bucket = storage_client.bucket(bucket_name)
    type_num = -1
    if art_type == "clayworks":
        type_num = 1
    elif art_type == "drawings":
        type_num = 2
    elif art_type == "paintings":
        type_num = 3
    elif art_type == "geography":
        type_num = 4
    elif art_type == "digital":
        type_num = 5
    sql_query = "SELECT source FROM images WHERE type = " + str(type_num)

    conn = GcdMysqlConnector()
    result = conn.perform_query(sql_query)
    print(sql_query)

    urls = []
    for res in result:
        blob = bucket.blob(res[0])
        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 30 minutes
            expiration=datetime.timedelta(minutes=30),
            # Allow GET requests using this URL.
            method="GET",
        )
        urls.append(url)
    return urls


def generate_random_display_image_links(bucket_name):
    storage_client = get_google_authentication()
    bucket = storage_client.bucket(bucket_name)
    sql_query = "SELECT name, source FROM images WHERE recommend = 1 ORDER BY RAND() LIMIT 5;"

    conn = GcdMysqlConnector()
    print(sql_query)
    result = conn.perform_query(sql_query)

    output = []
    for res in result:
        blob = bucket.blob(res[1])
        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 30 minutes
            expiration=datetime.timedelta(minutes=30),
            # Allow GET requests using this URL.
            method="GET",
        )
        output.append({"name": res[0], "signed_url": url})
    return output
