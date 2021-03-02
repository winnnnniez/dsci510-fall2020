import requests
import json
import pandas as pd

def get_api_content(keyword, api_key):
    """takes two string arguments: keyword and api_key,
    returns a list of dictionaries converted by json format containing data from nookipedia api

    Str, Str -> List"""

    url = f'https://api.nookipedia.com/{keyword}?api_key={api_key}'
    content = requests.get(url).json()
    return content

# get villagers information from nookipedia api
def extract_villagers_info():
    """returns a list of dictionaries of Animal Crossing: New Horizons villagers' information

    None -> List"""

    keyword = 'villagers'
    api_key = '80e27fa5-02ee-4bf2-a86f-b4899fcfe8a2'
    content = get_api_content(keyword, api_key)

    villagers_acnh = list()
    for el in content:
        # villagers that appears in Animal Crossing: New Horizons
        if 'NH' in el['appearances']:
            villagers_acnh.append(el)

    return villagers_acnh

def save_to_json(list_of_dict):
    """takes a list of dictionaries,
    saves it to a json file in the 'data' folder

    List -> None"""

    with open('data/raw_villagers_info.json', 'w') as json_file:
        json.dump(list_of_dict, json_file)

def modeling_villagers_info(info_list):
    """takes a list of dictionaries (raw_villagers_info)
    returns a dataframe that has been modeled

    List -> DataFrame"""

    df_raw = pd.DataFrame(info_list)
    # change 'Renée' to 'Renee' for easier processing later
    df_raw.loc[df_raw['name'] == 'Renée', 'name'] = 'Renee'
    # keeps the name and four features of villagers that may influence their popularity
    df_villagers_info = df_raw[['name', 'species', 'personality', 'gender', 'sign']]
    return df_villagers_info

def save_to_csv(df):
    """takes a dataframe,
    saves it to csv file in the 'data' folder

    DataFrame -> None"""

    df.to_csv('data/modeled_villagers_info.csv', index=False)
