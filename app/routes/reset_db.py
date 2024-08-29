from app.app import app, db


@app.route('/resett')
def reset():
    # Dropping all collections
    db.dropAllCollections()

    return 'Database reset successfully'