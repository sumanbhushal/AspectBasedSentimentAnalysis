import urllib
import re

def wiki_crawler(product_entity):
    base_url = 'https://en.wikipedia.org'
    entity_url = base_url + '/'+ product_entity
