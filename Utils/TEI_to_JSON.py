import sys
import xml.etree.ElementTree as ET

def transformer_TEI_JSON(tei):

    root = ET.fromstring(tei)

    ref_dict = {}
    dic_author = {}
    list_title = []
    list_idno = []
    list_authors = []
    list_editor = []
    dic_biblScope = {}
    dic_date = {}
    dic_page = {}
    dic_editor = {}
    error = []

    for main_child in root:
        for child in main_child:
            if child.tag == 'title':
                if child.attrib:
                    list_title.append([child.text,child.attrib])
            elif child.tag == 'author':
                for persname in list(child):
                    for child in persname:
                        if child.attrib:
                            dic_author[child.tag + f'_{list(child.attrib.values())[0]}']=child.text
                        else:
                            dic_author[child.tag] = child.text
                list_authors.append(dic_author)
            elif child.tag == 'idno':
                if child.attrib:
                    ref_dict[list(child.attrib.values())[0]] = child.text
                else:
                    list_idno.append(child.text)
            elif child.tag == 'imprint':
                for child in list(child):
                    if child.tag == "biblScope":
                        dic_biblScope[list(child.attrib.values())[0]] = child.text
                        if list(child.attrib.values())[0] == 'page':
                            for attrib, values in child.attrib.items():
                                if attrib != 'unit':
                                    dic_page[attrib] = values
                            dic_biblScope['page'] = dic_page
                    if child.tag == "date":
                        dic_date['date_text'] = child.text
                        for item, values in child.attrib.items():
                            dic_date[item] = values
            elif child.tag == 'editor':
                for persname in list(child):
                    for child in persname:
                        if child.attrib:
                            dic_editor[child.tag + f'_{list(child.attrib.values())[0]}']=child.text
                        else:
                            dic_editor[child.tag] = child.text
                list_editor.append(dic_editor)
            elif child.tag == "meeting":
                ref_dict['meeting'] = child.text

            else:
                error.append(child)

        ref_dict['titles'] = list_title
        ref_dict['idno'] = list_idno
        ref_dict['authors'] = list_authors
        ref_dict['editor'] = list_editor
        ref_dict['date'] = dic_date
        ref_dict['bibscope'] = dic_biblScope
    return [ref_dict, error]



tei_test = """
  <biblStruct xml:id="b16">
        <analytic>
                <title level="a" type="main">Simple embedding for link prediction in knowledge graphs</title>
                <author>
                        <persName><forename type="first">Seyed</forename><surname>Mehran</surname></persName>
                </author>
                <author>
                        <persName><forename type="first">Kazemi</forename></persName>
                </author>
                <author>
                        <persName><forename type="first">David</forename><surname>Poole</surname></persName>
                </author>
        </analytic>
        <monogr>
                <title level="m">Proceedings of NeurIPS</title>
                <meeting>NeurIPS</meeting>
                <imprint>
                        <date>2018</date>
                </imprint>
        </monogr>
</biblStruct>

"""

transformer_TEI_JSON(tei_test)