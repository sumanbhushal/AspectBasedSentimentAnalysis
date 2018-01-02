from django.shortcuts import render
from .models import SentimentAnalysis, Sentences, ExecutionTime
from django.db.models import Sum

def index(request):
    """
    Return result form database to view to render them.
    :param request: web request
    :return: return web response with all data need in index page
    """
    pie_chart_overall_postive_score = SentimentAnalysis.objects.aggregate(Sum('pos_score'))
    pie_chart_overall_negative_score = SentimentAnalysis.objects.aggregate(Sum('neg_score'))
    pie_chart_overall_neutral_score = SentimentAnalysis.objects.aggregate(Sum('neu_score'))
    print(pie_chart_overall_postive_score, pie_chart_overall_negative_score, pie_chart_overall_neutral_score )
    feature_bar_graph = SentimentAnalysis.objects.all().order_by('-pos_score')[0:10]
    feature_for_tag_cloud = SentimentAnalysis.objects.all()
    feature_for_structure_summ = SentimentAnalysis.objects.all().order_by('-pos_score')[0:10]
    ex_duration = ExecutionTime.objects.all().first()

    return render(request, 'productsentiment/home.html', {"aspect_bar_graph": feature_bar_graph,
                                                          "aspect_tag_cloud": feature_for_tag_cloud,
                                                          "asepct_structure_summary": feature_for_structure_summ,
                                                          "overall_positive_score": pie_chart_overall_postive_score,
                                                          "overall_negative_score": pie_chart_overall_negative_score,
                                                          "overall_neutral_score": pie_chart_overall_neutral_score,
                                                          "execution_duration": ex_duration})

def page(request, aspect):
    """
    Get the apsect name from web and return the aspect details extracting from database
    :param request: web request
    :param aspect: name of aspect
    :return: return web response with aspect detail
    """
    aspect_details = SentimentAnalysis.objects.get(product_aspect=aspect)

    # Positive sentences
    if(aspect_details.pos_sent_ids!=''):
        pos_sentence_list = get_senteces_by_id(aspect_details.pos_sent_ids)
    else:
        pos_sentence_list = ['Positive sentences not found']

    # Negative sentences
    if(aspect_details.neg_sent_ids!=''):
        neg_sentence_list = get_senteces_by_id(aspect_details.neg_sent_ids)
    else:
        neg_sentence_list = ['Negative sentences not found']

    # Neutral Sentences
    if (aspect_details.neu_sent_ids != ''):
        neu_sentence_list = get_senteces_by_id(aspect_details.neu_sent_ids)
    else:
        neu_sentence_list = ['Neutral sentences not found']

    ex_duration = ExecutionTime.objects.all().first()

    return render(request, 'productsentiment/includes/DetailView.html', {"aspect_details": aspect_details,
                                                                         "pos_sentence": pos_sentence_list,
                                                                         "neg_sentence": neg_sentence_list,
                                                                         "neu_sentence": neu_sentence_list,
                                                                         "execution_duration": ex_duration
                                                                         })

def get_senteces_by_id(sent_ids):
    """
    Get sentence by its id
    :param sent_ids: sentence id
    :return: sentence
    """
    sentence_list = []
    sent_id_list = (sent_ids).split(",")
    for sentence_id in sent_id_list:
        sentence_list.append(Sentences.objects.get(sentences_id=sentence_id))
    return sentence_list

