from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS
from views.client_views import client_views
from views.item_views import item_views
from views.order_views import order_views
from views.vehicle_views import vehicle_views

app = Flask(__name__)
FlaskJSON(app)

# # enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(client_views)
app.register_blueprint(item_views)
app.register_blueprint(order_views)
app.register_blueprint(vehicle_views)

if __name__ == '__main__':
    app.run()
