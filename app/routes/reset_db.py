from app.app import app, db

@app.route('/resett')
def reset():
    db.dropAllCollections()
    return '<br>'.join('reset')