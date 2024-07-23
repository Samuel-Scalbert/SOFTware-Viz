from flask import Flask, render_template
from pyArango.connection import Connection
from Utils.db import insert_json_db
from Utils.dashboard import dashboard
import sys

app = Flask(__name__,template_folder='templates',static_folder='static')

app.config['ARANGO_HOST'] = 'localhost'
app.config['ARANGO_PORT'] = 8529
app.config['ARANGO_DB'] = 'SOF-viz'
app.config['ARANGO_USERNAME'] = 'root'
app.config['ARANGO_PASSWORD'] = 'root'

def init_db():
    global db
    db = Connection(
        arangoURL='http://{host}:{port}'.format(
            host=app.config['ARANGO_HOST'],
            port=app.config['ARANGO_PORT']
        ),
        username=app.config['ARANGO_USERNAME'],
        password=app.config['ARANGO_PASSWORD']
    )[app.config['ARANGO_DB']]
try:
    init_db()  # Call the init_db function to initialize the db variable
except:
    sys.exit(1)
insert_json_db('./app/static/data/json_files/from_xml','./app/static/result/XML_meta_software', db)
structure = None
global data_dashboard
data_dashboard = None
#data_dashboard = dashboard(db, structure)

from app.routes import doc_route, dashboard_route,reset_db, software_route, api_route, disambiguate_route

@app.route('/')
def home():
    return render_template('partials/conteneur.html')

