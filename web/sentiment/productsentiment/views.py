from django.shortcuts import render
import json
from .models import SentimentAnalysis

def index(request):
    feature_bar_graph = SentimentAnalysis.objects.all().order_by('-pos_score')[1:11]
    feature_for_tag_cloud = SentimentAnalysis.objects.all()
    feature_for_structure_summ = SentimentAnalysis.objects.all().order_by('-pos_score')[0:10]

    return render(request, 'productsentiment/home.html', {"aspect_bar_graph": feature_bar_graph,
                                                          "aspect_tag_cloud": feature_for_tag_cloud,
                                                          "asepct_structure_summary": feature_for_structure_summ})

def page(request, id):
    feature_for_structure_summ = SentimentAnalysis.objects.get(id=id)

    return render(request, 'productsentiment/DetailView.html', {"asepct_structure_summary": feature_for_structure_summ})