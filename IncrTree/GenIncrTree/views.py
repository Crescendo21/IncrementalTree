from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import openai

openai.api_key = settings.OPENAI_API_KEY

def index(request):
    if request.method == 'POST':
        base_idea = request.POST.get('base_idea')
        increment_logic = request.POST.get('increment_logic')

        # Traiter les données du formulaire ici (appeler l'API, générer l'arbre, etc.)

        request.session['base_idea'] = base_idea
        request.session['increment_logic'] = increment_logic

        if 'unique_ideas_history' not in request.session:
            request.session['unique_ideas_history'] = []

        request.session['unique_ideas_history'].append(base_idea)

        return redirect('result')

    elif request.method == 'GET':
        request.session['unique_ideas_history'] = []

    return render(request, 'GenIncrTree/index.html')


def result(request):
    base_idea = request.session.get('base_idea')
    increment_logic = request.session.get('increment_logic')

    return render(request, 'GenIncrTree/result.html', {'base_idea': base_idea, 'increment_logic': increment_logic})

# Ajoutez la nouvelle route pour générer des idées avec l'API d'OpenAI
def generate_ideas(request):
    clicked_word = request.GET.get('clicked_word')
    increment_logic = request.GET.get('increment_logic')

    if 'unique_ideas_history' not in request.session:
        request.session['unique_ideas_history'] = []

    unique_ideas_history = request.session['unique_ideas_history']
    print("mon historique :",unique_ideas_history)

    prompt = f"Donne moi un cinq {increment_logic} unique et concis, séparé par une virgule, différents des unes des autres pour : {clicked_word} qui ne sont pas dans cette liste (ne porte pas attention à la ponctuation, n'ajoute pas de puce ou de numéros en début de phrase ou mot) : {unique_ideas_history}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Get the generated ideas from the first choice and split them by commas
        ideas_text = response.choices[0].text.strip()
        unique_ideas_list = ideas_text.split(',')

        print("mes idées:", unique_ideas_list)
        print("incrementation logique :", increment_logic)
        print("mot cliqué", clicked_word)

        unique_ideas_history.extend(unique_ideas_list)
        request.session['unique_ideas_history'] = unique_ideas_history

        return JsonResponse({'ideas': unique_ideas_list})

    except Exception as e:
        return JsonResponse({'error': str(e)})

def diagram(request):
    return render(request, 'GenIncrTree/diagram.html')

