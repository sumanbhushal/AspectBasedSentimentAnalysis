import xml.etree.ElementTree as et
import config, msc, database

def read_dataset():
    xml_file = config.DATASETS_PATH + "Restaurants.xml"

    tree = et.parse(xml_file)
    root = tree.getroot()

    manual_annoted_aspects = []
    sentence_list = []
    i=0
    for sentence in root:
        if(i < 500):
            if(sentence.tag == "sentence"):
                for attr in sentence:
                    # print(attr.tag)
                    if (attr.tag == "text"):
                        sentence_list.append(attr.text)
                    if (attr.tag == "aspectTerms"):
                        for a in attr:
                            # print(a.attrib.get('term'))
                                manual_annoted_aspects.append(a.attrib.get('term'))
        i += 1

    # print(len(manual_annoted_aspects), manual_annoted_aspects)
    new_list = []
    for aspect_term in manual_annoted_aspects:
        count = manual_annoted_aspects.count(aspect_term)
        if (aspect_term not in new_list and count >= 5):
            new_list.append(aspect_term.lower())
    print(len(new_list), new_list)

    for new_asp in new_list:
        msc.write_to_file("Restaurant_ml.txt", new_asp + '\n')

    # database.insert_domain_data_into_review_table(sentence_list)
    # database.insert_sentence_into_sentence_table()
    # sent_list_from_db = database.fetch_sentence_from_sentence_table()
    # for sentence in sentence_list:
    #     msc.write_to_file("Restaurant_dataset.txt", sentence.lower() + '\n')

read_dataset()