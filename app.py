from flask import Flask
from flask_json import as_json, FlaskJSON
from flask_cors import CORS


app = Flask(__name__)
FlaskJSON(app)

# # enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/clients')
@as_json
def get_clients():
    return {"rows": [
              {
                   "client_name": 'John Smith',
                    "address": 'Fake Street 123',
                    "distance": 20
              },
              {
                    "client_name": 'Hans Schmidt',
                    "address": 'Fake Street 556',
                    "distance": 60
              },
              {
                    "client_name": 'Mary Jane',
                    "address": 'Fake Street 1230',
                    "distance": 60
              }],
            "headers": [
                {
                    "text": 'Client Name',
                    "value": 'client_name'
                },
                {
                    "text": 'Address',
                    "value": 'address'
                }

            ]
    }


if __name__ == '__main__':
    app.run()
