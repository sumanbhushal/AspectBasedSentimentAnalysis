
def precision(extracted_aspect, actual_aspect):
    """
    Calculate precision
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # precision = extracted_aspect intersection actual_aspect/extracted_aspect
    precision = abs(extracted_aspect-actual_aspect)/extracted_aspect
    return precision


def recall(extracted_aspect, actual_aspect):
    """
    Calculate recall
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # recall = extracted_aspect intersection actual_aspect/actual_aspect
    recall = abs(extracted_aspect-actual_aspect)/actual_aspect
    return recall


def f_measure(precision, recall):
    """
    Calculate f-measure
    :param precision:
    :param recall:
    :return:
    """
    # f-measure = 2 *  precision * recall / precision + recall
    f_measure = (2*precision*recall)/ (precision+recall)
    return f_measure