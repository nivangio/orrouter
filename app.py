from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS
from client_views import client_views

app = Flask(__name__)
FlaskJSON(app)

# # enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(client_views)

if __name__ == '__main__':
    app.run()
