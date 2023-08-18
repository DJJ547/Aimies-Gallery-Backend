import psycopg2

# url = urlparse.urlparse(os.environ['DATABASE_URL'])
DATABASE_URL = "postgres://mlyzxuchslnfql:cc3a1eef9b761a5aca9f1c036e60efdc144e4ece4a829cd1fbd93cb69485adbc@ec2-34-236-199-229.compute-1.amazonaws.com:5432/daginp0seb7nlr"


class HerokuPostgreSqlConnector:
    # def __init__(self):

    def execute_query(self, query):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        for r in result:
            print(r)
        cur.close()
        conn.close()
        return result
