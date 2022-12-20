import os


def create_controller_file_string(table_name):
    template = f'''  
                const {table_name} = require("../models/{table_name}.model.js");
                
                // Create and Save a new {table_name}
                exports.create = (req, res) => {{
                  // Validate request
                  if (!req.body) {{
                    res.status(400).send({{
                      message: "Content can not be empty!"
                    }});
                  }}
                
                  // Create a {table_name}
                  const model = new {table_name}(req.body);
                
                  // Save Tutorial in the database
                  {table_name}.create(model, (err, data) => {{
                    if (err)
                      res.status(500).send({{
                        message:
                          err.message || "Some error occurred while creating the Tutorial."
                      }});
                    else res.send(data);
                  }});
                }};
                
                // Retrieve all {table_name} from the database (with condition).
                exports.findAll = (req, res) => {{
              
                  {table_name}.getAll((err, data) => {{
                    if (err)
                      res.status(500).send({{
                        message:
                          err.message || "Some error occurred while retrieving tutorials."
                      }});
                    else res.send(data);
                  }});
                }};
                
                // Find a single {table_name} by Id
                exports.findOne = (req, res) => {{
                  {table_name}.findById(req.params.id, (err, data) => {{
                    if (err) {{
                      if (err.kind === "not_found") {{
                        res.status(404).send({{
                          message: `Not found {table_name} with id ${{req.params.id}}.`
                        }});
                      }} else {{
                        res.status(500).send({{
                          message: "Error retrieving {table_name} with id " + req.params.id
                        }});
                      }}
                    }} else res.send(data);
                  }});
                }};
                
                // Update a {table_name} identified by the id in the request
                exports.update = (req, res) => {{
                  // Validate Request
                  if (!req.body) {{
                    res.status(400).send({{
                      message: "Content can not be empty!"
                    }});
                  }}
                
                  console.log(req.body);
                
                  {table_name}.updateById(
                    req.params.id,
                    new {table_name}(req.body),
                    (err, data) => {{
                      if (err) {{
                        if (err.kind === "not_found") {{
                          res.status(404).send({{
                            message: `Not found {table_name} with id ${{req.params.id}}.`
                          }});
                        }} else {{
                          res.status(500).send({{
                            message: "Error updating {table_name} with id " + req.params.id
                          }});
                        }}
                      }} else res.send(data);
                    }}
                  );
                }};
                
                // Delete a Tutorial with the specified id in the request
                exports.delete = (req, res) => {{
                  {table_name}.remove(req.params.id, (err, data) => {{
                    if (err) {{
                      if (err.kind === "not_found") {{
                        res.status(404).send({{
                          message: `Not found {table_name} with id ${{req.params.id}}.`
                        }});
                      }} else {{
                        res.status(500).send({{
                          message: "Could not delete {table_name} with id " + req.params.id
                        }});
                      }}
                    }} else res.send({{ message: `{table_name} was deleted successfully!` }});
                  }});
                }};
                

        '''
    return template


def create_controllers(db_info, path):
    table_names = set([i['TABLE_NAME'] for i in db_info])

    for i in table_names:
        controller_file_string = create_controller_file_string(i)
        controller_file_path = os.path.join(path, 'app', 'controllers', i + '.controller.js')

        with open(controller_file_path, 'w') as file:
            file.write(controller_file_string)
