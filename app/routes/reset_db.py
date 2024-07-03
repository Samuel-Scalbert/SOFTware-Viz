from app.app import app, db

@app.route('/resett')
def reset():
    db.dropAllCollections()
    db.dropAllEdges()
    return '<br>'.join('reset')