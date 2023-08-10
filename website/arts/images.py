import datetime
from website.gcd.GoogleStorageClient import get_google_authentication
from website.gcdmysql.GcdMysqlConnector import GcdMysqlConnector
from website.gcdmysql.constant import PATH
from website.gcd.GoogleStorageClient import get_google_authentication



def generate_image_names_and_links(bucket_name, art_type):
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
    sql_query = "SELECT name,source FROM images WHERE type = " + str(type_num)

    conn = GcdMysqlConnector()
    result = conn.perform_query(sql_query)
    print(sql_query)

    names_and_links = []
    for res in result:
        blob = bucket.blob(res[1])
        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 30 minutes
            expiration=datetime.timedelta(minutes=30),
            # Allow GET requests using this URL.
            method="GET",
        )
        names_and_links.append({"name": res[0], "signed_url": url})
    return names_and_links


def generate_random_display_image_links(bucket_name):
    storage_client = get_google_authentication()
    bucket = storage_client.bucket(bucket_name)
    sql_query = "SELECT name, source FROM images WHERE recommend = 1 ORDER BY RAND() LIMIT 5;"

    conn = GcdMysqlConnector()
    print(sql_query)
    result = conn.perform_query(sql_query)

    output = {
        "errors": False,
        "names": [],
        "urls": []
    }
    for res in result:
        name = res[0]
        blob = bucket.blob(res[1])
        signed_url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 30 minutes
            expiration=datetime.timedelta(minutes=30),
            # Allow GET requests using this URL.
            method="GET",
        )
        output["names"].append(name)
        output["urls"].append(signed_url)
    return output
