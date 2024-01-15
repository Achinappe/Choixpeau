from math import sqrt
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
