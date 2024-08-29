from app.app import db
from rapidfuzz import fuzz
from flask import url_for


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


def api_list_software(list_software):
    dict_software = {}
    query = f"""
            FOR software IN softwares
                FILTER software.software_name.normalizedForm in {list_software} or software.software_name.rawForm in {list_software}
                LET context = software.context
                LET forms = [software.software_name.normalizedForm, software.software_name.rawForm]
                LET offset =  [software.software_name.offsetStart,software.software_name.offsetEnd]
                FOR edge IN edge_software
                FILTER software._id == edge._to
                LET doc = document(edge._from)
                    RETURN [doc.file_hal_id, context, offset, forms]
            """
    list_context_halid = db.AQLQuery(query, rawResults=True)
    for context in list_context_halid:
        if context[0] in dict_software.keys():
            dict_software[context[0]].append([context[1], context[2], context[3]])
        else:
            dict_software[context[0]] = [[context[1], context[2],context[3]]]

    html_content = ""
    html_title = ""
    for key, value in dict_software.items():
        html_context= ""
        for context in value:
            context_html = ("<div class='list-context'>" + context[0][:context[1][0]] + f"<div class='software_item' name='{context[2][1]}'>" +
                context[0][context[1][0]:context[1][1]] + "</div>" + context[0][context[1][1]:] + f"<span style='color: blue'>(Rawform: '{context[2][0]}',Normalizedform: '{context[2][1]}')</span>" +"</div>")
            html_context += context_html
        html_title += f"<h4><a href='{ url_for('doc_info',doc_id=key) }'>{key}</a></h4>{html_context}"
    html_content = f"<div class='document_dis_context'>{html_title}</div>"
    return html_content