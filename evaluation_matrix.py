
def precision(extracted_aspect, actual_aspect):
    """
    Calculate precision
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # precision = extracted_aspect intersection actual_aspect/extracted_aspect
    precision_value = abs(extracted_aspect - actual_aspect) / extracted_aspect
    return precision_value


def recall(extracted_aspect, actual_aspect):
    """
    Calculate recall
    :param extracted_aspect:
    :param actual_aspect:
    :return:
    """
    # recall = extracted_aspect intersection actual_aspect/actual_aspect
    recall_value = abs(extracted_aspect - actual_aspect) / actual_aspect
    return recall_value


def f_measure(precision, recall):
    """
    Calculate f-measure
    :param precision:
    :param recall:
    :return:
    """
    # f-measure = 2 *  precision * recall / precision + recall
    f_measure_value = (2 * precision * recall) / (precision + recall)
    return f_measure_value