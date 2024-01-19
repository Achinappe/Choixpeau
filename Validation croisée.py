from math import sqrt
from random import randint
import csv

with open("Characters.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characters_tab = [{key : value.replace('\xa0', ' ') for key, value in element.items()} for element in reader]


with open("Caracteristiques_des_persos.csv", mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    characteristics_tab = [dico for dico in reader]

updated_characters_tab = []
for kaggle_character in characters_tab:
    for poudlard_character in characteristics_tab:
        if poudlard_character['Name'] == kaggle_character['Name']:
            kaggle_character.update(poudlard_character)
            updated_characters_tab.append(kaggle_character)

def indexation(tab):
    index_id_characteristics = {int(character['Id']): 
                                 (character['Name'],
                                 character['House'],
                                 int(character['Courage']),
                                 int(character['Ambition']),
                                 int(character['Intelligence']),
                                 int(character['Good'])) 
                                for character in tab}
    return index_id_characteristics

            
def creation_donnees_test(tab):
    joueurs_test = []
    copie_joueurs = tab[:]
    for _ in range(len(copie_joueurs) // 4):
        joueurs_test.append(copie_joueurs.pop(randint(0, len(copie_joueurs) - 1)))
    return joueurs_test, copie_joueurs

def distance(joueur1, joueur_cible, methode='euclidienne'):
    return int(sqrt((int(joueur1['Courage']) - int(joueur_cible['Courage']))** 2 
                          + (int(joueur1['Ambition']) - int(joueur_cible['Ambition']))** 2 
                          + (int(joueur1['Intelligence']) - int(joueur_cible['Intelligence']))** 2 
                          + (int(joueur1['Good']) - int(joueur_cible['Good']))** 2))

def ajout_distances(tab, joueur_inconnu):
    for joueur in tab:
        joueur['Distance'] = distance(joueur_inconnu, joueur)
    return tab

def best_house(tab):
    houses = {}
    for voisin in tab:
        if voisin['House'] in houses:
            houses[voisin['House']] += 1
        else:
            houses[voisin['House']] = 1
    maximum = 0
    for house, nb in houses.items():
        if nb > maximum:
            maximum = nb
            top_house = house
    return top_house

nb_tests = 100
temp = 0

for k in range(1, 31):
    bingo = 0
    for test in range(nb_tests):
        joueurs_test, joueurs_reference = creation_donnees_test(updated_characters_tab)
        for joueur_cible in joueurs_test:
            joueurs_reference = ajout_distances(joueurs_reference, joueur_cible)
            voisins = sorted(joueurs_reference, key=lambda x: x['Distance'])
            if best_house(voisins[:k]) == joueur_cible['House']:
                bingo += 1
        if bingo > temp:
            temp = bingo
            meilleur_k = k

    print(f"Pourcentage de réussite avec k = {k} : {round(bingo / len(joueurs_test))}")
print(f"La meilleure valeur de k est : {meilleur_k}")


characteristics = [{'Courage' : 9, 'Ambition' : 2, 'Intelligence' : 8, 'Good' : 9},
                   {'Courage' : 6, 'Ambition' : 7, 'Intelligence' : 9, 'Good' : 7},
                   {'Courage' : 3, 'Ambition' : 8, 'Intelligence' : 6, 'Good' : 3},
                   {'Courage' : 2, 'Ambition' : 3, 'Intelligence' : 7, 'Good' : 8},
                   {'Courage' : 3, 'Ambition' : 4, 'Intelligence' : 8, 'Good' : 8}]
for valeur in characteristics:
    distance_jj = ajout_distances(updated_characters_tab, valeur)
    resultat = sorted(distance_jj, key=lambda x: x['Distance'])
    house_result = best_house(resultat[:meilleur_k])
    print(f"La meilleur maison pour le personnage dont le profil est de {valeur['Courage']} de courage,"
          f" {valeur['Ambition']} d'ambition, {valeur['Intelligence']} d'intelligence "
          f"et de {valeur['Good']} de bonté est : {house_result}")
choix_courage = int(input("Saisissez une valeur de courage : "))
choix_ambition = int(input("Saisissez une valeur d'ambition : "))
choix_intelligence = int(input("Saisissez une valeur d'intelligence : "))
choix_bonte = int(input("Saisissez une valeur de bonté : "))

chosen_characteristics = {'Courage' : choix_courage, 'Ambition' : choix_ambition, 'Intelligence' : choix_intelligence, 'Good' : choix_bonte}

custom_distance = ajout_distances(updated_characters_tab, chosen_characteristics)
custom_result = sorted(custom_distance, key=lambda x: x['Distance'])
custom_house_result = best_house(custom_result[:meilleur_k])
print(f"La meilleur maison pour le personnage dont le profil est de {chosen_characteristics['Courage']} de courage,"
      f" {chosen_characteristics['Ambition']} d'ambition, {chosen_characteristics['Intelligence']} d'intelligence "
      f"et de {chosen_characteristics['Good']} de bonté est : {custom_house_result}")

