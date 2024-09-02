from app.app import db

def author_info_from_id(author_halauthorid):
    query = f"""
                 for auth in authors
                    filter auth.id.halauthorid ==  "{author_halauthorid}"
                    return auth
                    """

    author_info_data = db.AQLQuery(query, rawResults=True)
    return author_info_data