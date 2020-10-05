from django.shortcuts import render
import requests
from .forms import WordForm
import os


def index(request):
    form = WordForm()
    return render(request, 'apidict/index.html', {"form":form})




def results(request):
    context = {}
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word'].lower()
    else:
        form = WordForm()
    # Querying the scrapper
    # token = os.environ.get('owlbot_token') #probably does not allow any other form
    headers = {
        'Authorization': 'Token 6b192155a82dc6d94d6cf06dd2b913eaed0daca7',
    }
    response = requests.get(
        f'https://owlbot.info/api/v4/dictionary/{word}', headers=headers)
    context["word"] = word
    if response.status_code in range(200, 299):
        data = response.json()
        # attaching the defn list to the context
        context["results"] = data["definitions"]
    #return the view
    return render(request, 'apidict/results.html', context)


# def results(request):
#     context = {}
#     if request.method == 'POST':
#         form = WordForm(request.POST)
#         if form.is_valid():
#             word = form.cleaned_data['word']
#     else:
#         form = WordForm()
    

#     # Querying the scrapper
#     headers = {
#         'Authorization': 'Token 6b192155a82dc6d94d6cf06dd2b913eaed0daca7',
#     }
#     response = requests.get(
#         f'https://owlbot.info/api/v4/dictionary/{word}', headers=headers)
#     if response.status_code in range(200, 299):
#         data = response.json()
#         results = data["definitions"]
#         defn = []
#         for i in results:
#             definitions = {}
#             types = i["type"]
#             definition = i["definition"]
#             definitions["types"] = types
#             definitions["definition"] = definition
#             defn.append(definitions)
#         context["definition"] = defn #attaching the defn list to the context
        
#     print(context)
    
#     #return the view
#     return render(request, 'apidict/results.html', context)

