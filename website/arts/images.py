import datetime
from website.gcd.GoogleStorageClient import get_google_authentication
from website.postgreDatabase.HerokuPostgreSqlConnector import HerokuPostgreSqlConnector
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
    sql_query = 'SELECT name,source FROM "aimiefungart-utilities".art_images WHERE type = ' + str(type_num)

    conn = HerokuPostgreSqlConnector()
    result = conn.execute_query(sql_query)
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
    print(bucket)
    sql_query = 'SELECT name, source FROM "aimiefungart-utilities".art_images WHERE recommended = 1 ORDER BY random() LIMIT 5'

    conn = HerokuPostgreSqlConnector()
    print(sql_query)
    result = conn.execute_query(sql_query)
    print(result)

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
