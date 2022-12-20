from sqlalchemy import create_engine


def get_db_information(database,server,username,password):
    engine = create_engine(f"mariadb+pymysql://{username}:{password}@{server}/{database}", echo=False)

    with engine.connect() as conn:
        result = conn.execute(f"SELECT * FROM information_schema.`COLUMNS` c WHERE TABLE_SCHEMA = '{database}'")
        rows = result.fetchall()
        keys = [ i for i in result.keys()]
        fields = []
        for row in rows:
            dict = {}
            for i, column in enumerate(row):
                dict[keys[i]] = column
            fields.append(dict)
    return fields


if __name__ == '__main__':
    get_db_information()