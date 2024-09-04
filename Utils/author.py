from app.app import db

def author_info_from_id(author_halauthorid):
    query = f"""
        LET auth = (
            FOR author IN authors
                FILTER author.id.halauthorid == "{author_halauthorid}"
                RETURN author
        )
        
        LET softwareDocs = (
            FOR edge_doc IN edge_author
                FILTER edge_doc._to == auth[0]._id
                FOR edge_soft in edge_software
                FILTER edge_soft._from == edge_doc._from
                LET software = DOCUMENT(edge_soft._to)
                LET doc = DOCUMENT(edge_doc._from)
                RETURN [software.software_name.normalizedForm, doc.file_hal_id]
        )
        
        RETURN {{
            author: auth[0],
            software_names: UNIQUE(softwareDocs)
        }}
    """

    author_info_data = db.AQLQuery(query, rawResults=True)
    print(author_info_data)
    return author_info_data