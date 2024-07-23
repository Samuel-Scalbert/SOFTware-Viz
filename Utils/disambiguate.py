from app.app import db
from rapidfuzz import fuzz

def desambiguate_from_software(software):
    query = f'''
                for software in softwares
                return distinct software.software_name.normalizedForm
                '''
    list_software = list(db.AQLQuery(query, rawResults=True, batchSize=2000))
    list_possible_dup = []
    for software_available in list_software:
        ratio = fuzz.ratio(software_available, software)
        if software != software_available and ratio > 60:
            token_ratio = fuzz.token_sort_ratio(software, software_available)
            partial_ratio = fuzz.partial_ratio(software_available, software)
            average_ratio = (token_ratio+partial_ratio+ratio)/3
            if average_ratio > 80:
                list_possible_dup.append(software_available)
    return list_possible_dup