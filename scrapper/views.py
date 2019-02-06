from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urlsplit, urlunsplit, quote
from urllib.request import Request, urlopen
from django.views.decorators.csrf import csrf_exempt

authorizations = [
    '98901234'
]

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results,
                                                                          language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text


@csrf_exempt
def google(request):

   
    if (request.META['HTTP_AUTHORIZATION'] not in authorizations):
        return JsonResponse({'success': False, 'data': "UnAuthorized"});

    temp = request.POST.get('query')
    temp = quote(temp)

    url = 'https://www.google.com/search?q='+temp

    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        webpage = requests.get(url, headers=header)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'success': False, 'data': none});

    soup = BeautifulSoup(webpage.content, 'lxml')

    related_questions = []

    results = soup.findAll("div", {"class": "card-section"})
    for r in results:
        value=r.findAll("div", {"class": "brs_col"})
        for c in value:
            value2=c.findAll("p", {"class": "nVcaUb"})
            for c in value2:
                related_questions.append(c.a.text)


    return JsonResponse({'success' : True, 'data' : related_questions});
