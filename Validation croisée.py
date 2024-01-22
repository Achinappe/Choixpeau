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

            
def experimental_data_creation(tab):
    test_characters = []
    characters_copy = tab[:]
    for _ in range(len(characters_copy) // 4):
        test_characters.append(characters_copy.pop(randint(0, len(characters_copy) - 1)))
    return test_characters, characters_copy

def distance(character1, target_character, methode='euclidienne'):
    return int(sqrt((int(character1['Courage']) - int(target_character['Courage']))** 2 
                          + (int(character1['Ambition']) - int(target_character['Ambition']))** 2 
                          + (int(character1['Intelligence']) - int(target_character['Intelligence']))** 2 
                          + (int(character1['Good']) - int(target_character['Good']))** 2))

def distance_addition(tab, unknown_character):
    for character in tab:
        character['Distance'] = distance(unknown_character, character)
    return tab

def best_house(tab):
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

test_nb = 100
temp = 0

for k in range(1, 31):
    bingo = 0
    for test in range(test_nb):
        test_characters, characters_remaining = experimental_data_creation(updated_characters_tab)
        for target_character in test_characters:
            characters_remaining = distance_addition(characters_remaining, target_character)
            neighbours = sorted(characters_remaining, key=lambda x: x['Distance'])
            if best_house(neighbours[:k]) == target_character['House']:
                bingo += 1
        if bingo > temp:
            temp = bingo
            best_k = k

    print(f"Pourcentage de réussite avec k = {k} : {round(bingo / len(test_characters))}")
print(f"La meilleure valeur de k est : {best_k}")


characteristics = [{'Courage' : 9, 'Ambition' : 2, 'Intelligence' : 8, 'Good' : 9},
                   {'Courage' : 6, 'Ambition' : 7, 'Intelligence' : 9, 'Good' : 7},
                   {'Courage' : 3, 'Ambition' : 8, 'Intelligence' : 6, 'Good' : 3},
                   {'Courage' : 2, 'Ambition' : 3, 'Intelligence' : 7, 'Good' : 8},
                   {'Courage' : 3, 'Ambition' : 4, 'Intelligence' : 8, 'Good' : 8}]
for profile in characteristics:
    distance_tab = distance_addition(updated_characters_tab, profile)
    result = sorted(distance_tab, key=lambda x: x['Distance'])
    house_result = best_house(result[:best_k])
    print(f"La meilleur maison pour le personnage dont le profil est de {profile['Courage']} de courage,"
          f" {profile['Ambition']} d'ambition, {profile['Intelligence']} d'intelligence "
          f"et de {profile['Good']} de bonté est : {house_result}")
courage_choice = int(input("Saisissez une valeur de courage : "))
ambition_choice = int(input("Saisissez une valeur d'ambition : "))
intelligence_choice = int(input("Saisissez une valeur d'intelligence : "))
good_choice = int(input("Saisissez une valeur de bonté : "))

chosen_characteristics = {'Courage' : courage_choice, 'Ambition' : ambition_choice, 'Intelligence' : intelligence_choice, 'Good' : good_choice}

custom_distance = distance_addition(updated_characters_tab, chosen_characteristics)
custom_result = sorted(custom_distance, key=lambda x: x['Distance'])
custom_house_result = best_house(custom_result[:best_k])
print(f"La meilleur maison pour le personnage dont le profil est de {chosen_characteristics['Courage']} de courage,"
      f" {chosen_characteristics['Ambition']} d'ambition, {chosen_characteristics['Intelligence']} d'intelligence "
      f"et de {chosen_characteristics['Good']} de bonté est : {custom_house_result}")

