from django.shortcuts import render
import json
from .models import SentimentAnalysis, Sentences
from django.http import HttpResponse

def index(request):
    feature_bar_graph = SentimentAnalysis.objects.all().order_by('-pos_score')[1:11]
    feature_for_tag_cloud = SentimentAnalysis.objects.all()
    feature_for_structure_summ = SentimentAnalysis.objects.all().order_by('-pos_score')[0:10]

    return render(request, 'productsentiment/home.html', {"aspect_bar_graph": feature_bar_graph,
                                                          "aspect_tag_cloud": feature_for_tag_cloud,
                                                          "asepct_structure_summary": feature_for_structure_summ})

def page(request, aspect):
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

    return render(request, 'productsentiment/includes/DetailView.html', {"aspect_details": aspect_details,
                                                                         "pos_sentence": pos_sentence_list,
                                                                         "neg_sentence": neg_sentence_list,
                                                                         "neu_sentence": neu_sentence_list
                                                                         })

def get_senteces_by_id(sent_ids):
    sentence_list = []
    sent_id_list = (sent_ids).split(",")
    for sentence_id in sent_id_list:
        sentence_list.append(Sentences.objects.get(sentences_id=sentence_id))
    return sentence_list

