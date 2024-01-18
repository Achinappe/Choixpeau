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
            
#print(updated_characters_tab)
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
    return int(round(sqrt((int(joueur1['Courage']) - int(joueur_cible['Courage']))** 2 + (int(joueur1['Ambition']) - int(joueur_cible['Ambition']))** 2 + (int(joueur1['Intelligence']) - int(joueur_cible['Intelligence']))** 2 + (int(joueur1['Good']) - int(joueur_cible['Good']))** 2)))

def ajout_distances(tab, joueur_inconnu):
    for joueur in tab:
        joueur['Distance'] = distance(joueur_inconnu, joueur)
    return tab
'''
def plusprochevoisin(characteristics):
    dico_distance = []
    for joueur in updated_characters_tab:
        distance = int(round(sqrt((int(joueur['Courage']) - characteristics[0])** 2 + (int(joueur['Ambition']) - characteristics[1])** 2 + (int(joueur['Intelligence']) - characteristics[2])** 2 + (int(joueur['Good']) - int(characteristics[3]))** 2)))
        dico_distance.append([joueur['Name'], distance, joueur['House']])
        dico_distance.sort(key=lambda x: x[1], reverse=False)
    return dico_distance
#print(plusprochevoisin((9, 9, 9, 9)))


resultat = plusprochevoisin((9, 9, 9, 9))
dico_ppvoisin = {'Griffondor' : 0, 'Poufsouffle' : 0, 'Serdaigle' : 0, 'Serpentard' : 0}
for i in range(5):
    print(f"{resultat[i][0]}, de la maison {resultat[i][2]} est un des plus proches voisins du profil ")
    if resultat[i][2] == 'Gryffindor':
        dico_ppvoisin['Griffondor'] += 1
    elif resultat[i][2] == 'Hufflepuff':
        dico_ppvoisin['Poufsouffle'] += 1
    elif resultat[i][2] == 'Ravenclaw':
        dico_ppvoisin['Serdaigle'] += 1
    else:
        dico_ppvoisin['Serpentard'] += 1
key_list = [k  for (k, val) in dico_ppvoisin.items() if val == max(dico_ppvoisin.values())]
print(f"Le profil saisi semble plus adapté pour intégrer la maison {str(key_list[0])}")
'''
def meilleur_poste(tab):
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

for k in range(1, 31):
    bingo = 0
    for test in range(nb_tests):
        joueurs_test, joueurs_reference = creation_donnees_test(updated_characters_tab)
        for joueur_cible in joueurs_test:
            joueurs_reference = ajout_distances(joueurs_reference, joueur_cible)
            voisins = sorted(joueurs_reference, key=lambda x: x['Distance'])
            if meilleur_poste(voisins[:k]) == joueur_cible['House']:
                bingo += 1
    print(f"Pourcentage de réussite avec k = {k} : {round(bingo / len(joueurs_test))}")
'''
copie_joueurs = creation_donnees_test(updated_characters_tab)[1]
joueurs_test = creation_donnees_test(updated_characters_tab)[0]
print(copie_joueurs)
print("\n\n\n\n")
print(joueurs_test)
def ajout_distances(tab, joueur_inconnu):
    for joueur in tab:
        joueur['Distance'] = distance(joueur_inconnu, joueur)
    return tab
'''