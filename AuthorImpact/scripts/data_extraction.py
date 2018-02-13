import xml.etree.ElementTree as etree

#this script is extracting the  relavant data from the xml file

if __name__ == "__main__":

    path_file_data = '../data/dblp-data.xml'
    file_out_type_object = '../data/type_object.txt'
    file_out_relation_author_of = '../data/relation_author_of.txt'
    file_out_relation_cites = '../data/relation_cites.txt'
    file_out_relation_journal = '../data/relation_journal.txt'
    file_out_relation_book = '../data/relation_book.txt'
    file_out_relation_preeceding = '../data/relation_proceeding.txt'
    file_out_relation_name_publisher = '../data/name_publisher.txt'
    file_out_relation_name_author = '../data/name_author.txt'
    file_out_relation_title_paper = '../data/title_paper.txt'

    with open(path_file_data, 'r') as fdata:

        tree = etree.parse(fdata)
        root = tree.getroot()
        #root[0] containes objects id
        #root[1] containes links
        #root[2] contains attributes as follows: ['object-type', 'conference', 'isbn', 'name', 'publisher', 'school','series', 'title', 'url', 'volume', 'year', 'link-type', 'month', 'number', 'pages', 'in-volume', 'in-year']
        #type of object-type  {'paper', 'proceedings', 'www', 'msthesis', 'phdthesis', 'person', 'journal', 'book'}

        child_object_type_attribute = [child for child in root[2] if child.attrib['NAME'] == 'object-type'][0]
        assert (child_object_type_attribute.attrib['ITEM-TYPE'] == 'O')

        #################################### extract the type of object #########################################
        filter = set(['paper', 'proceedings', 'person', 'journal', 'book'])
        #create list of id for different objects only for the above category
        child_object_type_attribute_with_values_str = [','.join([item.attrib['ITEM-ID'], item2.text.strip()])
                                                       for item in child_object_type_attribute for item2 in item if item2.text.strip() in filter ]
        # write the list
        with open(file_out_type_object, 'w') as fout:
            fout.write('id,name\n')
            fout.write('\n'.join(child_object_type_attribute_with_values_str))

        #######################################################################################


        #################################### author relation #########################################
        # extract the info related to the name of the author, name is an object attribute
        child_name_type = [child for child in root[2] if child.attrib['NAME'] == 'name'][0]
        assert (child_name_type.attrib['ITEM-TYPE'] == 'O')
        # extract the name of the authors
        l_name = [','.join([element_value.attrib['ITEM-ID'], element_value[0].text]) for element_value in
                  child_name_type]
        # write the list of names
        with open(file_out_relation_name_author, 'w') as fout:
            fout.write('id,name\n')
            fout.write('\n'.join(l_name))
        #######################################################################################

        #################################### title relation #########################################


        # extract the attributes related to the  title of the papers, title is an object attribute
        child_title_type = [child for child in root[2] if child.attrib['NAME'] == 'title'][0]
        assert (child_name_type.attrib['ITEM-TYPE'] == 'O')
        # extract the name of the papers that are not proceedings, proceeding set is extracted above
        l_title = [','.join([element_value.attrib['ITEM-ID'], element_value[0].text.replace(',', ' ')]) for
                   element_value in child_title_type]
        # write the title
        with open(file_out_relation_title_paper, 'w') as fout:
            fout.write('id,name\n')
            fout.write('\n'.join(l_title))
        #######################################################################################


        #extract all the links relations
        l_link = [list(map(int,[item.attrib['ID'],item.attrib['O1-ID'], item.attrib['O2-ID']])) for item in root[1]]

        # extract the attributes for the links
        child_link_type_attribute = [child for child in root[2] if child.attrib['NAME'] == 'link-type'][0]
        assert (child_link_type_attribute.attrib['ITEM-TYPE'] == 'L')


        #################################### link author of and cite relations #########################################


        #extract the relation  author_of
        l_link_author_of = [int(element_value.attrib['ITEM-ID']) for element_value in child_link_type_attribute if
                            element_value[0].text == 'author-of']

        # extract the relations cites
        l_link_cites = [int(element_value.attrib['ITEM-ID']) for element_value in child_link_type_attribute if
                            element_value[0].text == 'cites']


        #check the data
        intersection_link_author_of = set([item[0] for item in l_link]).intersection(set(l_link_author_of))
        intersection_link_cite_of = set([item[0] for item in l_link]).intersection(set(l_link_cites))

        assert(len(intersection_link_author_of) == len(l_link_author_of))
        assert(len(intersection_link_cite_of) == len(l_link_cites))

        set_l_author_of = set(l_link_author_of)
        set_l_cites = set(l_link_cites)

        assert (len(l_link_cites) == len(set_l_cites))
        assert (len(l_link_author_of) == len(set_l_author_of))


        # filtering the link list considering only the relations author of
        l_str_link_author_of = [','.join(list(map(str, item))) for item in l_link
                                if item[0] in set_l_author_of]
        # filtering the link list considering only the relations cite
        l_str_link_cites = [','.join(list(map(str, item))) for item in l_link if item[0] in set_l_cites]

        # write the data
        with open(file_out_relation_author_of, 'w') as fout:
            fout.write('id,id_l,id_r\n')
            fout.write('\n'.join(l_str_link_author_of))

        with open(file_out_relation_cites, 'w') as fout:
            fout.write('id,id_l,id_r\n')
            fout.write('\n'.join(l_str_link_cites))

        #######################################################################################

        #################################### proceceeding,book, journal and publisher relations #########################################


        # extract the id related to the publisher
        child_publisher_type = [child for child in root[2] if child.attrib['NAME'] == 'publisher'][0]
        assert (child_publisher_type.attrib['ITEM-TYPE'] == 'O')
        # extract the name of the publisher
        list_publisher = [','.join([element_value.attrib['ITEM-ID'], element_value[0].text.replace(',', ' ')]) for element_value in
                          child_publisher_type]

        with open(file_out_relation_name_publisher, 'w') as fout:
            fout.write('id,name\n')
            fout.write('\n'.join(list_publisher))

        # extract the id of the in-proceeding type of link
        l_link_in_proceedings = [int(element_value.attrib['ITEM-ID']) for element_value in child_link_type_attribute if
                                 element_value[0].text == 'in-proceedings']

        l_link_in_jounal = [int(element_value.attrib['ITEM-ID']) for element_value in child_link_type_attribute if
                                 element_value[0].text == 'in-journal']

        l_link_in_collection = [int(element_value.attrib['ITEM-ID']) for element_value in child_link_type_attribute if
                                 element_value[0].text == 'in-collection']

        intersection_in_proceedings = set([item[0] for item in l_link]).intersection(set(l_link_in_proceedings))
        assert (len(intersection_in_proceedings) == len(l_link_in_proceedings))
        set_l_in_proceedings = set(l_link_in_proceedings)
        assert (len(set_l_in_proceedings) == len(l_link_in_proceedings))

        intersection_in_jounal = set([item[0] for item in l_link]).intersection(set(l_link_in_jounal))
        assert (len(intersection_in_jounal) == len(l_link_in_jounal))
        set_l_in_jounal = set(l_link_in_jounal)
        assert (len(set_l_in_jounal) == len(l_link_in_jounal))

        intersection_in_collection = set([item[0] for item in l_link]).intersection(set(l_link_in_collection))
        assert (len(intersection_in_collection) == len(l_link_in_collection))
        set_l_in_collection = set(l_link_in_collection)
        assert (len(set_l_in_collection) == len(l_link_in_collection))


        #filtering the link list considering only the relations proceeding,book an journal
        l_link_in_proceedings = [ ','.join(list(map(str,item))) for item in l_link if
                                     item[0] in set_l_in_proceedings]

        l_link_in_journal = [ ','.join(list(map(str,item))) for item in l_link if
                                 item[0] in set_l_in_jounal]

        l_link_in_book = [ ','.join(list(map(str,item))) for item in l_link if
                             item[0] in set_l_in_collection]

        with open(file_out_relation_preeceding, 'w') as fout:
            fout.write('id,id_l,id_r\n')
            fout.write('\n'.join(l_link_in_proceedings))

        with open(file_out_relation_journal, 'w') as fout:
            fout.write('id,id_l,id_r\n')
            fout.write('\n'.join(l_link_in_journal))

        with open(file_out_relation_book, 'w') as fout:
            fout.write('id,id_l,id_r\n')
            fout.write('\n'.join(l_link_in_book))








