import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

def get_web_content(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, features='html.parser')
    content.close()
    return soup

# ranking list web scraping
def extract_ranking_list():
    """returns a list of dictionaries, dictionaries contain:
    {'name':string, 'ranking':string of number, 'image':string, link to the character's image}

    None -> List"""

    url = 'https://gamewith.net/animal-crossing-new-horizons/article/show/18171'
    soup = get_web_content(url)
    # find the main table
    table = soup.find('div', {'class': 'w-instant-database-list'})

    characters = list()
    for el in table.find_all('tr', {'class': 'w-idb-element'}):
        character = dict()

        # find values of the dictionary
        name = el['data-col1']
        ranking = el.find('th').text
        image = el.find('img')['data-original']

        # assign values to keys
        character['name'] = name
                            # only remain numbers in the string for 'ranking'
        character['ranking'] = re.sub('[^0-9]', '', ranking)
        character['image'] = image
        characters.append(character)
    return characters

def save_to_json(list_of_dict):
    """takes a list of dictionaries,
    saves it to a json file in the 'data' folder

    List -> None"""

    with open('data/raw_characters_ranking.json', 'w') as json_file:
        json.dump(list_of_dict, json_file)

def modeling_villagers_ranking(ranking_list, df_villagers_info):
    """takes a list of dictionaries (raw_characters_ranking) and df_villagers_info as reference
    returns a dataframe that has been modeled

    List, DataFrame -> DataFrame"""

    # select villagers from Animal Crossing: New Horizons among the 451 characters in the ranking list
    #  villages_ranking contains 391 villagers with their ranking and image url
    villagers_ranking = list()
    for el in ranking_list:
        if el['name'] in df_villagers_info.values:
            villagers_ranking.append(el)
        # name of Sprinkle is different in villagers_info data (Sprinkle)
        elif el['name'] == 'Sprinkles':
            villagers_ranking.append(el)

    df_raw = pd.DataFrame(villagers_ranking)
    # change the name 'Sprinkles' to 'Sprinkle' to match villagers_info data
    df_raw['name'] = df_raw['name'].replace('Sprinkles', 'Sprinkle')
    # re-assign the ranking to avoid gaps caused by removing characters
    df_raw['ranking'] = range(1,392)

    df_villagers_ranking = df_raw
    return df_villagers_ranking

def save_to_csv(df):
    """takes a dataframe,
    saves it to csv file in the 'data' folder

    DataFrame -> None"""

    df.to_csv('data/modeled_villagers_ranking.csv', index=False)
