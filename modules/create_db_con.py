import os


def create_db_con(base_path, database, server,username,password):
    con_file_string = f'''
    const mysql = require("mysql");

    var connection = mysql.createPool({{
        host: '{server}',
        user: '{username}',
        password: '{password}',
        database: '{database}'
    }});

    module.exports = connection;
    '''

    db_con_path = os.path.join(base_path, 'app', 'config', 'db.config.js')

    with open(db_con_path, 'w') as file:
        file.write(con_file_string)

