import os


def create_route_file_string(table_name):
    template =  f'''
    module.exports = app => {{
      const {table_name} = require("../controllers/{table_name}.controller.js");
    
      var router = require("express").Router();
    
      // Create a new {table_name}
      router.post("/", {table_name}.create);
      
      // Retrieve all {table_name}
      router.get("/", {table_name}.findAll);
      
      // Retrieve a single {table_name} with id
      router.get("/:id", {table_name}.findOne);
    
      // Update a {table_name} with id
      router.put("/:id", {table_name}.update);
    
      // Delete a {table_name} with id
      router.delete("/:id", {table_name}.delete);
    
    
      app.use('/api/{table_name}', router);
    }};
    '''
    return template


def create_routes(db_info, path):
    table_names = set([i['TABLE_NAME'] for i in db_info])

    for i in table_names:
        route_file_path = os.path.join(path, 'app', 'routes', i + '.routes.js' )
        route_file_string = create_route_file_string(i)
        with open(route_file_path, 'w') as file:
            file.write(route_file_string)




