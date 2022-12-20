import os
import shutil



def project_setup(base_path,project_name):
    ### crate api dir
    path = os.path.join(base_path, project_name)

    if os.path.exists(path):
        shutil.rmtree(path)

    os.mkdir(path)

    os.chdir(path)
    os.system('npm init -y')
    os.system('npm install express mysql cors')


    os.mkdir(os.path.join(path, 'app'))
    os.mkdir(os.path.join(path, 'app', 'config'))
    os.mkdir(os.path.join(path, 'app', 'models'))
    os.mkdir(os.path.join(path,  'app', 'controllers'))
    os.mkdir(os.path.join(path,  'app', 'routes'))
    return path