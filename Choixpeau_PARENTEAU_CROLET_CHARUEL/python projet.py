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

from random import randint
from browser import html, document, window
import csv

choix_son = window.prompt("Cette page est sonore ! Voulez vous désactiver le son ? \n1. Oui\n2. Non")

#importation des personnages, des caractéristiques et des questions
def importation(nom_fichier: str) -> list:
    '''
    Importe les données à partir d'un fichier CSV.
    Entrée : nom_du_fichier, str
    Sortie : donnees, table 
    '''
    if nom_fichier == "Characters.csv":
        with open(nom_fichier, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            donnees = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]
    else:
        with open(nom_fichier, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            donnees = [dico for dico in reader]
    return donnees

#création des différentes tables
dico_questions = importation("Question.csv")
characters_tab = importation("Characters.csv")
characteristics_tab = importation("Caracteristiques_des_persos.csv")



#fusion de tables
updated_characters_tab = []
for kaggle_character in characters_tab:
    for poudlard_character in characteristics_tab:
        if poudlard_character['Name'] == kaggle_character['Name']:
            kaggle_character.update(poudlard_character)
            updated_characters_tab.append(kaggle_character)

def changer_k(ev):
    '''
    Permet de choisir une valeur de k personnalisée
    Entrée : ev, bouton cliqué
    Sortie : None
    '''
    global best_k
    best_k = int(input("Saisissez une nouvelle valeur de k : "))
document["k perso"].bind("click", changer_k)

#définitions de fonctions
def indexation(tab: list) -> dict:
    '''
    Indexe une table en entrée
    Entrée : tab, table à indexer
    Sortie : index_id_characteristics, table indexée
    '''
    houses_characters = {}
    
    for character in tab:
        house = character['House']
        if house not in houses_characters:
            houses_characters[house] = []
        houses_characters[house].append({
            'Id': character['Id'],
            'Name': character['Name'],
            'House': character['House'],
            'Courage': int(character['Courage']),
            'Ambition': int(character['Ambition']),
            'Intelligence': int(character['Intelligence']),
            'Good': int(character['Good'])
        })
    
    #ajuste le nombre d'élèves par maison
    min_characters_per_house = min(len(characters) for characters in houses_characters.values())
    
    selected_characters = []
    for characters in houses_characters.values():
        selected_characters.extend(characters[:min_characters_per_house])
    
    index_id_characteristics = {character['Id']: character for character in selected_characters}
    
    return index_id_characteristics


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

def demarrage_questionnaire(ev):
    '''
    Enclenche le début du questionnaire
    Entrée : ev, clic de bouton
    Sortie : None
    '''
    global progression_question
    #mise en place de l'espace du questionnaire
    document["Demarrage"].remove()
    document["espace_interactif"].clear()
    question = html.H3(dico_questions[progression_question]['Question'])
    question.id = "zone_question"
    document["espace_interactif"] <= question 
    #ajout de boutons contenant les réponses
    reponses = ['Reponse A', 'Reponse B', 'Reponse C']
    compteur = 1
    for reponse in reponses:
        bouton = html.BUTTON(dico_questions[progression_question][reponse], id=f"Reponse{compteur}", Class="glow-on-hover")
        compteur += 1     
        document["espace_interactif"] <= bouton
        document["espace_interactif"] <= html.B("<br>")
        document[bouton.id].bind("click", bouton_reponse)
    progression_question += 1

document["Demarrage"].bind("click", demarrage_questionnaire)

def reinitialiser_questionnaire(ev):
    '''
    Reinitialise le questionnaire
    Entrée : ev, bouton redémarrer cliqué
    Sortie : None
    '''
    global progression_question
    global bareme_global
    global best_k

    progression_question = 0
    bareme_global = {'Ambition': 0, 'Courage': 0, 'Good': 0, 'Intelligence': 0}
    best_k = 0
    #recréation du bouton démarrage et réinitialisation de l'affichage
    bouton_demarrage = html.BUTTON("Démarrer le questionnaire", id="Demarrage", Class="glow-on-hover")
    document["espace_interactif"] <= bouton_demarrage
    document["Demarrage"].bind("click", demarrage_questionnaire)
    document["display"].clear()
    document["display"] <= html.IMG(src='Dumbledore.gif', width=300, height=400, id="image")
    document["Redémarrage"].remove()

def bouton_reponse(ev):
    '''
    Change les réponses affichés par les boutons
    Entrée : ev, bouton réponse cliqué
    Sortie : None
    '''
    global progression_question
    global bareme_global
    bouton_id = ev.target.id
    if progression_question < 15:
        #changement du texte des boutons et de la question
        document["Reponse1"].textContent = dico_questions[progression_question]['Reponse A']
        document["Reponse2"].textContent = dico_questions[progression_question]['Reponse B']
        document["Reponse3"].textContent = dico_questions[progression_question]['Reponse C']
        document["zone_question"].html = dico_questions[progression_question]['Question']
        if bouton_id == "Reponse1":
            bareme_correspondant = 'Bareme A'    
        elif bouton_id == "Reponse2":
            bareme_correspondant = 'Bareme B'
        else:
            bareme_correspondant = 'Bareme C'
        #ajout des valeurs récupérées par le bareme dans la variable bareme_global
        bareme_brut = dico_questions[progression_question][bareme_correspondant]
        valeurs_bareme = tuple(bareme_brut.strip("()").split(","))
        bareme_global['Ambition'] += int(valeurs_bareme[0]) * 0.9
        bareme_global['Courage'] += int(valeurs_bareme[1]) * 0.9
        bareme_global['Good'] += int(valeurs_bareme[2])
        bareme_global['Intelligence'] += int(valeurs_bareme[3]) * 0.9
    else:
        #affichage de fin
        bareme_global = {key: bareme_global[key] // 4 for key in bareme_global.keys()}
        print(bareme_global)
        document["zone_question"].html = "Le questionnaire est fini !"
        document["image"].remove()
        document["Reponse1"].remove()
        document["Reponse2"].remove()
        document["Reponse3"].remove()
        resultat_maison = profil_personnalise(bareme_global)
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
        #création du bouton permettant le redémarrage
        bouton_redemarrage = html.BUTTON("Redémarrer le questionnaire ?", id="Redémarrage", Class="glow-on-hover")
        bouton_redemarrage.bind("click", reinitialiser_questionnaire)
        document["espace_interactif"] <= html.B("<br>")
        document["espace_interactif"] <= bouton_redemarrage


    progression_question += 1
    
def choix_caracteristiques(ev):
    '''
    Permet de choisir manuellement les valeurs associées aux caractéristiques
    Entrée : ev, bouton profil personnalisé cliqué
    Sortie : None
    '''
    courage_choice = int(input("Saisissez une valeur de courage : "))
    ambition_choice = int(input("Saisissez une valeur d'ambition : "))
    intelligence_choice = int(input("Saisissez une valeur d'intelligence : "))
    good_choice = int(input("Saisissez une valeur de bonté : "))

    given_characteristics = {'Courage': courage_choice, 'Ambition': ambition_choice,
                            'Intelligence': intelligence_choice, 'Good': good_choice}
    profil_personnalise(given_characteristics)

document["Profil personnalisé"].bind("click", choix_caracteristiques)

def profil_personnalise(chosen_characteristics: dict) -> str:
    '''
    Fait le résultat avec un profil personnalisé
    Entrée : ev, évènement qui déclenche la fonction
    Sortie : custom_house_result, maison déterminée par l'algorithme des kPPV
    '''
    global best_k
    if best_k == 0:
        best_k = 5

    #application de l'algorithme pour les valeurs personnalisées
    custom_distance = distance_addition(indexed_characters_tab, chosen_characteristics)
    custom_result = sorted(custom_distance, key=lambda x: x['Distance'])
    custom_house_result = best_house(custom_result[:best_k])
    document["espace_interactif"] <= html.B("<br>") + "Tes plus proches voisins sont : "
    for i in range(best_k):
        document["espace_interactif"] <= html.B("<br>") + f"- {custom_result[i]['Name']} de la maison {custom_result[i]['House']}"
    document["espace_interactif"] <= html.B("<br>") + f"Tu appartiens donc à la maison {custom_house_result} !"
    return custom_house_result


#définition de variables importantes
bareme_global = {'Ambition': 0, 'Courage': 0, 'Good': 0, 'Intelligence': 0}
indexed_characters_tab = indexation(updated_characters_tab)
best_k = 0
progression_question = 0