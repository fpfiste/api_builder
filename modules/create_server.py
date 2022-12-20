import os


def create_server_file_string(require_route_string, cors_origin, port):
    template = f'''
        const express = require("express");
        const cors = require("cors");

        const app = express();

        var corsOptions = {{
          origin: "{cors_origin}"
        }};

        app.use(cors(corsOptions));

        // parse requests of content-type - application/json
        app.use(express.json()); 

        // parse requests of content-type - application/x-www-form-urlencoded
        app.use(express.urlencoded({{ extended: true }}));

        // simple route
        app.get("/", (req, res) => {{
          res.json({{ message: "Welcome" }});
        }});

        {require_route_string}

        // set port, listen for requests
        const PORT = {port};
        app.listen(PORT, () => {{
          console.log(`Server is running on port ${{PORT}}.`);
        }});
    '''
    return template

def create_server(db_info, base_path,  cors_origin, port):
    table_names = set([i['TABLE_NAME'] for i in db_info])

    require_string = '\n'.join([f'require("./app/routes/{i}.routes.js")(app);' for i in table_names])

    server_file_string = create_server_file_string(require_string,  cors_origin, port)

    server_file_path = os.path.join(base_path, 'index.js')

    with open(server_file_path, 'w') as file:
        file.write(server_file_string)
