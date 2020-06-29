from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from starter import db_session

client_views = Blueprint("client_views", __name__)

@client_views.route('/clients', methods=['GET'])
@as_json
def get_clients():
    return {"rows": [
              {
                   "contact_person": 'John Smith',
                    "address": 'Fake Street 123',
                    "distance": 20
              },
              {
                    "contact_person": 'Hans Schmidt',
                    "address": 'Fake Street 556',
                    "distance": 60
              },
              {
                    "contact_person": 'Mary Jane',
                    "address": 'Fake Street 1230',
                    "distance": 60
              }],
            "headers": [
                {
                    "text": 'Contact Person',
                    "value": 'contact_person'
                },
                {
                    "text": 'Address',
                    "value": 'address'
                }

            ]
    }
