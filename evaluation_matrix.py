import config, re, pre_processing
import matplotlib.pyplot as plt

def precision(extracted_aspect_list):
    """
    Calculate precision
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # precision = extracted_aspect intersection actual_aspect/extracted_aspect
    actual_aspect = get_actual_aspect()
    extracted_aspect = []
    for aspect in extracted_aspect_list:
        # for count, aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    print("Extracted asepct", len(extracted_aspect),extracted_aspect)
    print("Actual Aspect", len(actual_aspect),actual_aspect)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)
    print("Match Aspect",len(ext_asp_intersection_actual),ext_asp_intersection_actual)
    precision_value = len(ext_asp_intersection_actual) / len(extracted_aspect)
    print(precision_value)
    asp_ext_intersection_actual = []
    asp_act_intersection_ext = []

    for asp in actual_aspect:
        if asp not in extracted_aspect:
            asp_ext_intersection_actual.append(asp)
    print("Not Match actual aspect", len(asp_ext_intersection_actual), asp_ext_intersection_actual)

    for asp in extracted_aspect:
        if asp not in actual_aspect:
            asp_act_intersection_ext.append(asp)
    print("Not Match expected", len(asp_act_intersection_ext), asp_act_intersection_ext)
    return precision_value


def recall(extracted_aspect_list):
    """
    Calculate recall
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # recall = extracted_aspect intersection actual_aspect/actual_aspect
    actual_aspect = get_actual_aspect()
    extracted_aspect = []
    for aspect in extracted_aspect_list:
        # for count, aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    print(len(extracted_aspect), extracted_aspect)
    print(len(actual_aspect), actual_aspect)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)
    print(len(ext_asp_intersection_actual), ext_asp_intersection_actual)
    recall_value = len(ext_asp_intersection_actual) / len(actual_aspect)
    print(recall_value)
    return recall_value


def f_measure(precision_value, recall_value):
    """
    Calculate f-measure
    :param precision:
    :param recall:
    :return:
    """
    # f-measure = 2 *  precision * recall / precision + recall
    print (precision_value, recall_value)
    f_measure_value = (2 * precision_value * recall_value) / (precision_value + recall_value)
    print("f-measure", f_measure_value)
    return f_measure_value


def get_actual_aspect():
    file = open(config.MANUAL_LABLED_ASPECT_PATH + "product_aspects_Canon G3_ml.txt", "r").read()
    actual_product = file.split('\n')
    # lemmatized = pre_processing.lemmatization(actual_product)
    # print("Lemma evaluation", len(lemmatized), lemmatized)
    return actual_product
