from django.shortcuts import render
import requests
from .forms import WordForm
import os


def scrapper(word):
    headers = {
        'Authorization': 'Token 6b192155a82dc6d94d6cf06dd2b913eaed0daca7',
    }
    response = requests.get(
        f'https://owlbot.info/api/v4/dictionary/{word}', headers=headers)
    if response.status_code in range(200, 299):
        data = response.json()
    return data


def index(request):
    form = WordForm()
    return render(request, 'apidict/index.html', {"form":form})


def synonyms(request):
    word_id = request.session.get('word')
    context = {}
    app_id = "050970e7"
    app_key = "863d4f01d8a7e5b8aa359bbe9c9436aa"
    language = "en-gb"
    
    
    url = (
        "https://od-api.oxforddictionaries.com:443/api/v2/entries/"
        + language
        + "/"
        + word_id
    )
    
    response = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    
    if response.status_code in range(200, 299):
        results = response.json()["results"]
        if ("synonyms" in results[0]["lexicalEntries"][0]["entries"][0]["senses"][0].keys()):
            synonyms_list = results[0]["lexicalEntries"][0]["entries"][0]["senses"][0]["synonyms"]
    context["word"] = word_id
    context["synonyms"] = synonyms_list
    print(synonyms_list)
    return render(request, 'apidict/synonyms.html',context)




def results(request):
    context = {}
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word'].lower()
    else:
        form = WordForm()
    # Querying the scrapper
    data=scrapper(word)
    
    # attaching the defn list to the context
    context["results"] = data["definitions"]
    context["word"] = word
    request.session["word"] = word
    
    #return the view
    return render(request, 'apidict/results.html', context)
