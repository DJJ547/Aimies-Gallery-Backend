from gcdmysql.GcdMysqlConnector import GcdMysqlConnector


def testgcdsql():
    db_name = "aimiefung-art"
    conn_name = "aimiefung-art-db:asia-east2:aimiefung-art"
    sql_query = "SELECT source FROM images"
    conn = GcdMysqlConnector()
    conn.perform_query(sql_query)


def main():
    testgcdsql()
    # coinbase_renkoscalp()
    # test_renko()


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s \n %(message)s',
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     handlers=[
    #         TimedRotatingFileHandler('renko_trade.log', when="midnight", interval=1,
    #                                  backupCount=100), logging.StreamHandler()],
    # )
    main()
