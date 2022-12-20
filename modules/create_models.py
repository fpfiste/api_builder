import os


def create_model_file_string(table_name, constructor_string, pk_field, insert_field_string,insert_place_holder_string, insert_value_string, update_field_string, update_value_string):
    model_template = f'''
        const sql = require("../config/db.config.js");

        // constructor
        const {table_name} = function({table_name}_object) {{
            {constructor_string}
        }};
        
        {table_name}.create = (newObject, result) => {{
          sql.query("INSERT INTO {table_name} ({insert_field_string}) VALUES ({insert_place_holder_string})", [{insert_value_string}], (err, res) => {{
            if (err) {{
              console.log("error: ", err);
              result(err, null);
              return;
            }}
        
            console.log("created {table_name}: ", {{ id: res.insertId, ...newObject }});
            result(null, {{ id: res.insertId, ...newObject }});
          }});
        }};
        
        {table_name}.findById = (id, result) => {{
          sql.query(`SELECT * FROM {table_name} WHERE {pk_field} = ?`,[id], (err, res) => {{
            if (err) {{
              console.log("error: ", err);
              result(err, null);
              return;
            }}
        
            if (res.length) {{
              console.log("found {table_name}: ", res[0]);
              result(null, res[0]);
              return;
            }}
        
            // not found {table_name} with the id
            result({{ kind: "not_found" }}, null);
          }});
        }};
        
        {table_name}.getAll = (result) => {{
          let query = "SELECT * FROM {table_name}";
        
          sql.query(query, (err, res) => {{
            if (err) {{
              console.log("error: ", err);
              result(null, err);
              return;
            }}
        
            console.log("tutorials: ", res);
            result(null, res);
          }});
        }};
        
        
        {table_name}.updateById = (id, newObject, result) => {{
          sql.query(
            "UPDATE {table_name} SET {update_field_string} WHERE {pk_field} = ?",
            [{update_value_string}],
            (err, res) => {{
              if (err) {{
                console.log("error: ", err);
                result(null, err);
                return;
              }}
        
              if (res.affectedRows == 0) {{
                // not found {table_name} with the id
                result({{ kind: "not_found" }}, null);
                return;
              }}
        
              console.log("updated {table_name}: ", {{ id: id, ...{table_name} }});
              result(null, {{ id: id, ...{table_name} }});
            }}
          );
        }};
        
        {table_name}.remove = (id, result) => {{
          sql.query("DELETE FROM {table_name} WHERE {pk_field} = ?", id, (err, res) => {{
            if (err) {{
              console.log("error: ", err);
              result(null, err);
              return;
            }}
        
            if (res.affectedRows == 0) {{
              // not found {table_name} with the id
              result({{ kind: "not_found" }}, null);
              return;
            }}
        
            console.log("deleted {table_name} with id: ", id);
            result(null, res);
          }});
        }};
        

        module.exports = {table_name};
        
        
        '''
    return model_template

def create_model_files(db_info, base_path):
    table_names = set([i['TABLE_NAME'] for i in db_info])
    for table in table_names:
        columns = [i for i in db_info if i['TABLE_NAME'] == table]
        constructor_string = '\n'.join([f'this.{i["COLUMN_NAME"]} = {table}_object.{i["COLUMN_NAME"]};' for i in columns])

        pk_field = [i['COLUMN_NAME'] for i in columns if i['COLUMN_KEY'] == 'PRI'][0]
        insert_field_string = ','.join([i['COLUMN_NAME'] for i in columns if i['COLUMN_KEY'] != 'PRI' ])
        insert_value_string = ','.join([f'newObject.{i["COLUMN_NAME"]}' for i in columns if i['COLUMN_KEY'] != 'PRI'])
        insert_placeholder_string = ','.join([ '?' for i in columns if i['COLUMN_KEY'] != 'PRI'])
        update_field_string = ','.join([f'{i["COLUMN_NAME"]} = ?' for i in columns if i['COLUMN_KEY'] != 'PRI'])
        update_value_string = insert_value_string + ',' + 'id'

        print(update_field_string)
        print(update_value_string)
        print('##################')

        model_file_string = create_model_file_string(table, constructor_string, pk_field, insert_field_string,insert_placeholder_string, insert_value_string, update_field_string, update_value_string)
        model_file_path = os.path.join(base_path, 'app', 'models', table +'.model.js')

        with open(model_file_path, 'w') as file:
            file.write(model_file_string)

