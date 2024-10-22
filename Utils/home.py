

def home_data(db):
    query = """
    LET doc = LENGTH(documents)

    LET soft = (
        FOR software IN softwares
            RETURN DISTINCT software.software_name.normalizedForm
    )
    
    LET url = (
        FOR url_soft IN softwares
        FILTER url_soft.url != null
            RETURN DISTINCT url_soft.url
    )
    
    LET ment = LENGTH(softwares)
    
    LET struc = LENGTH(structures)
    
    LET auth = LENGTH(authors)
    
    LET ref = LENGTH(references)
    
    RETURN {
        "documents_count": doc,
        "structures_count": struc,
        "authors_count": auth,
        "distinct_softwares_count": LENGTH(soft),
        "softwares_count": ment,
        "references_count": ref,
        "distinct_urls_count": LENGTH(url)
    }   
    """
    data = db.AQLQuery(query, rawResults=True)
    return data