from flask import Flask, render_template
from pyArango.connection import Connection
from Utils.db import insert_json_db
from Utils.home import home_data
app = Flask(__name__,template_folder='templates',static_folder='static')

app.config['ARANGO_HOST'] = 'arangodb'
#app.config['ARANGO_HOST'] = 'localhost'
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
    )
    if not db.hasDatabase('SOF-viz'):
        db.createDatabase('SOF-viz')
    db = Connection(
        arangoURL='http://{host}:{port}'.format(
            host=app.config['ARANGO_HOST'],
            port=app.config['ARANGO_PORT']
        ),
        username=app.config['ARANGO_USERNAME'],
        password=app.config['ARANGO_PASSWORD']
    )[app.config['ARANGO_DB']]

init_db()  # Call the init_db function to initialize the db variable

structure = None
global data_dashboard
data_dashboard = None
#data_dashboard = dashboard(db, structure)

from app.routes import doc_route, dashboard_route,reset_db, software_route, api_route, disambiguate_route, author_route, search_route, insert_json_route

@app.route('/')
def home():
    data = home_data(db)
    return render_template('pages/home.html', data=data[0])

