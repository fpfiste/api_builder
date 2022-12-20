import argparse

from modules import create_controllers
from modules import create_db_con
from modules import create_model_files
from modules import create_routes
from modules import create_server
from modules import get_db_information
from modules import project_setup



def build(path, db_info, database,server,username,password,  cors_origin, port):
    create_db_con(path, database, server,username,password)
    create_server(db_info, path,  cors_origin, port)
    create_routes(db_info, path)
    create_model_files(db_info, path)
    create_controllers(db_info, path)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', '--destination', dest='base_path', required=True, help='destination path of api folder')  # option that takes a value
    parser.add_argument('-n', '--name',dest='project_name', required=True,help='name of api project')
    parser.add_argument('-db', '--database', dest='database',required=True,help='name of the database with the tables')
    parser.add_argument('-s', '--server', dest='server', required=True,help='name of the server where the database is located')
    parser.add_argument('-u', '--username', dest='username',required=True, help='username of an account with access to the database')
    parser.add_argument('-pw', '--password', dest='password', required=True,help='password of an account with access to the database')
    parser.add_argument('-p', '--port', dest='port', required=True,help='port on which the api will be running')
    parser.add_argument('-co', '--cors', dest='cors_origin', required=True,help='cors_origin')

    args = parser.parse_args()
    path = project_setup(args.base_path, args.project_name)
    db_info = get_db_information(args.database, args.server,args.username, args.password)
    build(path, db_info, args.database, args.server,args.username, args.password,  args.cors_origin, args.port)



