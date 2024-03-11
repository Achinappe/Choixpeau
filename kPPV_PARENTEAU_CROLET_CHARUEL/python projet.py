# coding: utf-8
'''
Paul PARENTEAU-DENOEL
Alexandre CROLET
Arthur CHARUEL

Programme permettant d'exécuter l'algorithme des plus proches voisins des personnages d'Harry Potter

lien de la forge github : https://github.com/Achinappe/Choixpeau
Licence : CC-BY-HA
Version : 1.12.1
'''

from math import sqrt
from random import randint
from browser import html, document, window
import csv

choix_son = window.prompt("Cette page est sonore ! Voulez vous désactiver le son ? \n1. Oui\n2. Non")
with open("Question.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    DICO_Q = [dico for dico in reader]

#importation des personnages et des caractéristiques
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]


with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characteristics_tab = [dico for dico in reader]

#fusion de tables
updated_characters_tab = []
for kaggle_character in characters_tab:
    for poudlard_character in characteristics_tab:
        if poudlard_character['Name'] == kaggle_character['Name']:
            kaggle_character.update(poudlard_character)
            updated_characters_tab.append(kaggle_character)

def changer_k(ev):
    global best_k
    best_k = int(input("Saisissez une nouvelle valeur de k : "))
document["k perso"].bind("click", changer_k)

#définitions de fonctions
def indexation(tab: list) -> dict:
    '''
    Indexe une table en Entrée
    Entrée : tab, table à indexer
    Sortie : index_id_characteristics, table indexée
    '''
    index_id_characteristics = {character['Id']:
                                    {'Name' : character['Name'],
                                    'House' : character['House'],
                                    'Courage' : int(character['Courage']),
                                    'Ambition' : int(character['Ambition']),
                                    'Intelligence' : int(character['Intelligence']),
                                    'Good' : int(character['Good'])}
                                    for character in tab}
    return index_id_characteristics

def experimental_data_creation(support_tab: list) -> dict:
    '''
    Crée des données test à partir d'une table en Entrée
    Entrée : support_tab, table servant de support pour les données
    Sortie : test_characters, table indexée de personnages test, characters_copy, table indexée contenant les personnages restants
    '''
    test_characters = []
    characters_copy = support_tab[:]
    for _ in range(len(characters_copy) // 4):
        test_characters.append(characters_copy.pop(randint(0, len(characters_copy) - 1)))
    return indexation(test_characters), indexation(characters_copy)

def distance(character1: dict, target_character: dict, methode='euclidienne') -> float:
    '''
    Calcule la distance entre deux personnages
    Entrée : character1, personnage test; target_character, personnage à tester
    Sortie : target_character, personnage à test_characters
    '''
    return ((character1['Courage'] - target_character['Courage']) ** 2
                    + (character1['Ambition'] - target_character['Ambition']) ** 2
                    + (character1['Intelligence'] - target_character['Intelligence']) ** 2
                    + (character1['Good'] - target_character['Good']) ** 2) ** 0.5

def distance_addition(tab: dict, unknown_character: dict) -> list:
    '''
    Assemble toutes les distances calculées auparavant
    Entrée : tab, table de support; unknown_character, dictionnaire de personnage à tester 
    Sortie : distance_tab, table des distances avec les personnages
    '''
    distance_tab = []
    for character in tab.values():
        character['Distance'] = distance(unknown_character, character)
        distance_tab.append(character)
    return distance_tab

def best_house(tab: dict) -> str:
    '''
    Détermine la maison la plus adaptée pour un profil à partir d'une table de distances
    Entrée : tab, table des distances 
    Sortie : top_house, meilleure maison
    '''
    houses = {}
    for neighbour in tab:
        if neighbour['House'] in houses:
            houses[neighbour['House']] += 1
        else:
            houses[neighbour['House']] = 1
    maximum = 0
    for house, nb in houses.items():
        if nb > maximum:
            maximum = nb
            top_house = house
    return top_house

#définition de variables importantes
indexed_characters_tab = indexation(updated_characters_tab)
best_k = 0

def validation_croisee(ev):
    '''
    Effectue la validation croisée
    Entrée : ev, évènement qui déclenche la fonction
    Sortie : None
    '''
    global best_k
    document["texte_validation1"].html = ""
    document["texte_validation2"].html = ""
    test_nb = int(input("Saisissez le nombre de test à effectuer pour chaque valeur de k. Une valeur élevée permet une meilleure précision mais a un coût en performances"))
    temp = 0

    #exécution des test
    for k in range(1, 11, 2):
        bingo = 0
        for test in range(test_nb):
            test_characters, characters_remaining = experimental_data_creation(updated_characters_tab)
            for target_character in test_characters.values():
                characters_with_distances = distance_addition(characters_remaining, target_character)
                neighbours = sorted(characters_with_distances, key=lambda x: x['Distance'])
                if best_house(neighbours[:k]) == target_character['House']:
                    bingo += 1
            if bingo > temp:
                temp = bingo
                best_k = k        
        #affichage
        document["texte_validation1"].html += f"- Pourcentage de réussite avec k = {k} : {round(bingo / len(test_characters.values()), 2)} %<br>"
    document["texte_validation2"].textContent = f"La meilleure valeur de k est : {best_k}"


progression_question = 0

def demarrage(ev):
    global DICO_Q
    global progression_question
    document["Demarrage"].remove()
    document["espace_interactif"].clear()
    question = html.H3(DICO_Q[progression_question]['Question'])
    question.id = "zone_question"
    document["espace_interactif"] <= question 
    reponses = ['Reponse A', 'Reponse B', 'Reponse C']
    compteur = 1
    for reponse in reponses:
        button = document.createElement('button')
        button.textContent = DICO_Q[progression_question][reponse]
        button.id = f"Reponse{compteur}"
        compteur += 1
        button.classList.add("glow-on-hover")
        br = document.createElement('br')            
        document["espace_interactif"] <= button
        document["espace_interactif"] <= br
        document[button.id].bind("click", buttone)
    progression_question += 1

document["Demarrage"].bind("click", demarrage)
def reinitialiser_questionnaire(ev):
    global progression_question
    global bareme_global
    global best_k

    # Réinitialiser les variables
    progression_question = 0
    bareme_global = {'Ambition': 0, 'Courage': 0, 'Good': 0, 'Intelligence': 0}
    best_k = 0

    # Réinitialiser le HTML
    bouton_demarrage = html.BUTTON("Démarrer le questionnaire", id="Demarrage")
    bouton_demarrage.classList.add("glow-on-hover")
    document["espace_interactif"] <= bouton_demarrage
    document["Demarrage"].bind("click", demarrage)
    document["display"].clear()
    document["display"] <= html.IMG(src='Dumbledore.gif', width=300, height=400, id="image")
    document["Redémarrage"].remove()



bareme_global = {'Ambition': 0, 'Courage': 0, 'Good': 0, 'Intelligence': 0}

def buttone(ev):
    '''
    Fait des trucs
    '''
    global progression_question
    global DICO_QUESTION
    global bareme_global
    global choix_son
    bouton_id = ev.target.id
    if progression_question < 9:
        document["Reponse1"].textContent = DICO_Q[progression_question]['Reponse A']
        document["Reponse2"].textContent = DICO_Q[progression_question]['Reponse B']
        document["Reponse3"].textContent = DICO_Q[progression_question]['Reponse C']
        document["zone_question"].html = DICO_Q[progression_question]['Question']
        if bouton_id == "Reponse1":
            bareme_correspondant = 'Bareme A'    
        elif bouton_id == "Reponse2":
            bareme_correspondant = 'Bareme B'
        else:
            bareme_correspondant = 'Bareme C'
        pairs = [pair.strip() for pair in DICO_Q[progression_question][bareme_correspondant].split(',')]
        data_dict = dict(pair.split(':') for pair in pairs)
        data_dict = {key.strip(): int(value.strip()) for key, value in data_dict.items()}
        bareme_global = {key: bareme_global[key] + data_dict[key] / 5 for key in data_dict.keys()}
    else:
        document["zone_question"].html = "Le questionnaire est fini !"
        document["image"].remove()
        document["Reponse1"].remove()
        document["Reponse2"].remove()
        document["Reponse3"].remove()
        resultat_maison = profil_personnalise(bareme_global)
        document["espace_interactif"] <= f"Tu appartiens à la maison {resultat_maison} !"
        if resultat_maison == 'Gryffindor':
            document["display"] <= html.IMG(src='gryffondor.jpg', width=300, height=400)
            sound_file = 'gryffondor'
        elif resultat_maison == 'Slytherin':
            document["display"] <= html.IMG(src='serpentard.jpg', width=300, height=400)
            sound_file = 'serpentard'
        elif resultat_maison == 'Hufflepuff':
            document["display"] <= html.IMG(src='poufsouffle.gif', width=300, height=400)
            sound_file = 'poufsouffle'
        else:
            document["display"] <= html.IMG(src='serdaigle.gif', width=300, height=400)
            sound_file = 'serdaigle'
        if choix_son == '2':
                house_audio = html.AUDIO(src=f'{sound_file}.mp3', autoplay=True)
                house_audio.volume = 0.5
        bouton_redemarrage = document.createElement('button')
        bouton_redemarrage.classList.add("glow-on-hover")
        bouton_redemarrage.textContent = "Redémarrer le questionnaire ?"
        bouton_redemarrage.id = "Redémarrage"
        bouton_redemarrage.bind("click", reinitialiser_questionnaire)
        document["espace_interactif"] <= html.B("<br>")
        document["espace_interactif"] <= bouton_redemarrage


    progression_question += 1
    
def choix_caracteristiques(ev):
    courage_choice = int(input("Saisissez une valeur de courage : "))
    ambition_choice = int(input("Saisissez une valeur d'ambition : "))
    intelligence_choice = int(input("Saisissez une valeur d'intelligence : "))
    good_choice = int(input("Saisissez une valeur de bonté : "))

    given_characteristics = {'Courage': courage_choice, 'Ambition': ambition_choice,
                            'Intelligence': intelligence_choice, 'Good': good_choice}
    profil_personnalise(given_characteristics)

document["Profil personnalisé"].bind("click", choix_caracteristiques)

def profil_personnalise(chosen_characteristics):
    '''
    Fait le résultat avec un profil personnalisé
    Entrée : ev, évènement qui déclenche la fonction
    Sortie : None
    '''
    global best_k
    if best_k == 0:
        best_k = 5

    #application de l'algorithme pour les valeurs personnalisées
    custom_distance = distance_addition(indexed_characters_tab, chosen_characteristics)
    custom_result = sorted(custom_distance, key=lambda x: x['Distance'])
    custom_house_result = best_house(custom_result[:best_k])
    document["espace_interactif"].html <= (f"La meilleur maison pour le personnage dont le profil est de {chosen_characteristics['Courage']} de courage,"
            f" {chosen_characteristics['Ambition']} d'ambition, {chosen_characteristics['Intelligence']} d'intelligence "
            f"et de {chosen_characteristics['Good']} de bonté est : {custom_house_result}"
            f"<br>En effet, il a pour voisins :<br>")
    document["texte_profil_personnalisé"].html = "Tes plus proches voisins sont : "
    for i in range(best_k):
        document["texte_profil_personnalisé"].html += f"- {custom_result[i]['Name']} de la maison {custom_result[i]['House']}<br>"
    return custom_house_result
