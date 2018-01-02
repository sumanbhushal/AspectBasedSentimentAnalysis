import config, re, pre_processing
import matplotlib.pyplot as plt


def precision(extracted_aspect_list):
    """
    Calculate precision (precision = extracted_aspect intersection actual_aspect/extracted_aspect)
    :param extracted_aspect_list: List of extracted aspect
    :return: Precision value
    """

    # Get the manually annotated actual aspects from file
    actual_aspect = get_actual_aspect()

    extracted_aspect = []
    for aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)

    # Calculating precision
    precision_value = len(ext_asp_intersection_actual) / len(extracted_aspect)
    return precision_value


def recall(extracted_aspect_list):
    """
    Calculate recall (recall = extracted_aspect intersection actual_aspect/actual_aspect)
    :param extracted_aspect_list: List of extracted aspect
    :return: recall value
    """

    # Get the manually annotated actual aspects from file
    actual_aspect = get_actual_aspect()
    extracted_aspect = []
    for aspect in extracted_aspect_list:
        rg_exp_replace_space = re.compile('(\\s+)', re.IGNORECASE | re.DOTALL)
        aspect_replacing_space_with_underscore = re.sub(rg_exp_replace_space, '_', aspect)
        extracted_aspect.append(aspect_replacing_space_with_underscore)

    ext_asp_intersection_actual = []
    for ex_asp in extracted_aspect:
        if ex_asp in actual_aspect:
            ext_asp_intersection_actual.append(ex_asp)

    # Calculating recall value
    recall_value = len(ext_asp_intersection_actual) / len(actual_aspect)
    return recall_value


def f_measure(precision_value, recall_value):
    """
    Calculate f-measure (f-measure = 2 *  precision * recall / precision + recall)
    :param precision_value: Precision value
    :param recall_value: Recall value
    :return: F-measure
    """
    f_measure_value = (2 * precision_value * recall_value) / (precision_value + recall_value)
    return f_measure_value


def get_actual_aspect():
    """
    Read the file to get the manually annotated actual aspects from file
    :return: List of actual aspect
    """
    file = open(config.MANUAL_LABLED_ASPECT_PATH + "Canon G3_ml.txt", "r").read()
    actual_product = file.split('\n')
    lemmatized_aspect_list = pre_processing.lemmatization(actual_product)
    return lemmatized_aspect_list
